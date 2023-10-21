from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from channels.middleware import BaseMiddleware
from django.db import close_old_connections
from rest_framework.authtoken.models import Token
import json
from .models import CustomUser
from rest_framework import status
from rest_framework.response import Response


class WebSocketTokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        close_old_connections()
        scope["user"] = await self.get_user_from_token(scope)
        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user_from_token(self, scope):
        try:
            token = scope.get("headers").get(b"authorization").decode("utf-8")
            # Получить токен из заголовка "Authorization"
            token = token.split(" ")[1]
            user = Token.objects.get(key=token).user
            return user
        except (Token.DoesNotExist, IndexError, AttributeError):
            return None


class GetTokenNewRoleConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    @database_sync_to_async
    def get_token_new_role(self, role):
        user = User.objects.create()
        user.username = user.id
        user.save()
        custom_user = CustomUser.objects.create(user=user, role=role)
        token = Token.objects.create(user=user)
        token_key = token.key
        return token.key


    async def receive(self, text_data):
        print("receive performed")
        data = json.loads(text_data)
        action = data.get('action')
        role = data.get('data')
        if role in (1, 2) and action == 'new_role':
            token = await self.get_token_new_role(role)
            await self.send(text_data=json.dumps({"action": "new_role", "data": token}, ensure_ascii=False))
        else:
            await self.send(text_data=json.dumps({"action": "new_role", "data": "Неверная роль"}, ensure_ascii=False))


class BaseConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if user:
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        print("receive performed")
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'enter_user_data':
            # Здесь вы можете обработать ввод данных пользователя и записать их в базу данных
            # Например, вам понадобится извлечь пользователя на основе переданного токена
            user = self.scope['user']

            # Здесь обрабатывайте ввод данных, например:
            username = data.get('username')
            # Сохраните имя пользователя в базу данных
            user.username = username
            user.save()

        # Отправьте подтверждение клиенту
        await self.send(text_data=json.dumps({'message': 'Данные пользователя обновлены'}, ensure_ascii=False))
