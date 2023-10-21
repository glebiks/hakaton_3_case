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


""" 
консюмер для адмнистратора, выдает токен, 
по которому в систему сможет войти пользователь 
"""
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
        if role in (1, 2) and action == 'NEW_ROLE':
            token = await self.get_token_new_role(role)
            await self.send(text_data=json.dumps({"action": "NEW_ROLE", "data": token}, ensure_ascii=False))
        else:
            await self.send(text_data=json.dumps({"action": "NEW_ROLE", "data": "Неверная роль."}, ensure_ascii=False))


"""
консюмер нейминг полученного пользователем аккаунта и аутентификация по токену
"""
class BaseConsumer(AsyncWebsocketConsumer):

    user = None

    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            return Token.objects.get(key=token).user
        except Token.DoesNotExist:
            return None
        
    @database_sync_to_async
    def save_user_name(self, scope, username):
        try:
            self.user.username = username
            self.user.save()
        except:
            return None

    async def connect(self):
        token = self.scope['query_string'].decode('utf8').split('=')[1]
        self.user = await self.get_user_from_token(token)
        if self.user:
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        print("receive performed")
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'ENTER_NAME':
            username = data.get('data')
            await self.save_user_name(self, username)

        await self.send(text_data=json.dumps({'action': 'ENTER_NAME', 'data': 'Данные были обновлены.'}, ensure_ascii=False))
