from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from channels.middleware import BaseMiddleware
from django.db import close_old_connections
from rest_framework.authtoken.models import Token
import json
from .models import CustomUser, Table, Order, DishInOrder, Dish
from rest_framework import status
from rest_framework.response import Response
from .serializers import CustomUserSerializer, DishSerializer
from django.core import serializers


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

    @database_sync_to_async
    def get_token_new_role(self, role):
        user = User.objects.create()
        user.username = user.id
        user.save()
        custom_user = CustomUser.objects.create(user=user, role=role)
        token = Token.objects.create(user=user)
        token_key = token.key
        return token.key

    @database_sync_to_async
    def perform_data_for_table(self, table_id, table_status):
        table = Table.objects.get(id=table_id)
        table.status = table_status
        table.save()

    @database_sync_to_async
    def perform_i_serve(self, table_id):
        table = Table.objects.get(id=table_id)
        table.waiter = self.user
        table.save()

    @database_sync_to_async
    def perform_data_for_order(self, table_id, orders_from_request):
        table = Table.objects.get(id=table_id)
        order = Order.objects.create()
        table.order = order
        table.save()
        for dish_id in orders_from_request:
            DishInOrder.objects.create(to_order=order, dish=Dish.objects.get(id=dish_id))

    @sync_to_async
    def async_print(self, message):
        print(message)

    @sync_to_async
    def form_menu_data(self):
        data = Dish.objects.all()
        serializer = DishSerializer(data, many=True)
        json_data = serializer.data
        return json_data
    
    @sync_to_async
    def get_users_data(self):
        data = CustomUser.objects.all()
        serializer = CustomUserSerializer(data, many=True)
        json_data = serializer.data
        return json_data

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

        # создать нового официанта/повара
        """
            {
                "action": "NEW_ROLE",
                "data": 2
            }
        """
        role = data.get('data')
        if action == 'NEW_ROLE' and role in (1, 2):
            token = await self.get_token_new_role(role)
            await self.send(text_data=json.dumps({"action": "NEW_ROLE",
                                                  "data": {
                                                        "token": token,
                                                        "role": CustomUser.objects.get(user=self.user).role},
                                                  }, ensure_ascii=False))
        elif action == 'NEW_ROLE' and role not in (1, 2):
            await self.send(text_data=json.dumps({"action": "NEW_ROLE", "data": "Неверная роль."}, ensure_ascii=False))

        # войти новым пользователем и установить имя
        """
            {
                "action": "ENTER_NAME",
                "data": "Альберт"
            }
        """
        if action == 'ENTER_NAME':
            username = data.get('data')
            await self.save_user_name(self, username)
            await self.send(text_data=json.dumps({'action': 'ENTER_NAME', 'data': 'Данные были обновлены.'}, ensure_ascii=False))

        # управлять столиком, если ты официант
        """
            {
                "action": "MANAGE_TABLE",
                "data": {
                    "table_id": 4,
                    "table_status": 3,
                }
            }
        """
        if action == "MANAGE_TABLE":
            data = data.get("data")
            table_id = data["table_id"]
            table_status = data["table_status"]
            await self.perform_data_for_table(table_id, table_status)
            await self.send(text_data=json.dumps({"action": "MANAGE_TABLE", "data": "Статус столика был изменен."}, ensure_ascii=False))

        # взять на себя обслуживание столика
        """
        {
            "action": "I_SERVE",
            "data": 4
        }
        """
        if action == "I_SERVE":
            await self.perform_i_serve(data.get("data"))
            await self.send(text_data=json.dumps({"action": "I_SERVE", "data": "Официант взял столик."}, ensure_ascii=False))

        # просмотреть все меню
        """
        {
            "action": "SHOW_MENU"
        }
        """
        if action == "SHOW_MENU":
            temp_data = await self.form_menu_data()
            await self.send(text_data=json.dumps({"action": "SHOW_MENU", "data": temp_data}, ensure_ascii=False))

        # сделать заказ
        """
        {
            "action": "MAKE_ORDER",
            "data": {
                "table_id": 4,
                "order": [
                    1,
                    1,
                    2,
                    3
                ]
            }
        }
        """
        if action == "MAKE_ORDER":
            table_id = data.get("data")["table_id"]
            orders_from_request = data.get("data")["order"]
            await self.perform_data_for_order(table_id, orders_from_request)
            await self.send(text_data=json.dumps({"action": "MAKE_ORDER", "data": "Заказ создан."}, ensure_ascii=False))

        # получить список всех пользователей, если ты администратор
        """
        {
            "action": "GET_USERS"
        }
        """
        if action == "GET_USERS":
            temp_data = await self.get_users_data()
            await self.send(text_data=json.dumps({"action": "GET_USERS", "data": temp_data}, ensure_ascii=False))


        # изменить статус готовки блюда
        """
        {
            "action": "UPDATE_ORDER",
            "data": {
                "table_id": 4,
                "order": [
                    {
                        1
                    },
                    1,
                    2,
                    3
                ]
            }
        }
        """

        """
            "table_order": [
                {
                    "dish_id": 1,
                    "dish_status": 2,
                },
                {
                    "dish_in_order_id": 2,
                    "dish_status": 3,
                },
                {
                    "dish_in_order_id": 3,
                    "dish_status": 2,
                },
            ]
            table_order = data["table_order"]
        """
