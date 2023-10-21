import json
from channels.generic.websocket import AsyncWebsocketConsumer

class BaseConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("connect performed")
        await self.accept()

    async def disconnect(self, close_code):
        print("disconnect performed")
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
        await self.send(text_data=json.dumps({'message': 'Данные пользователя обновлены'}))
