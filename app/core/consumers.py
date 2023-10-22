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
from .serializers import CustomUserSerializer, DishSerializer, DishInOrderSerializer, TableSerializer
from django.core import serializers


class BaseConsumer(AsyncWebsocketConsumer):

    user = None
    custom_user = None

    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            return Token.objects.get(key=token).user
        except Token.DoesNotExist:
            return None

    @database_sync_to_async 
    def get_custom_user_from_user(self, user):
        try:
            return CustomUser.objects.get(user=user.id)
        except CustomUser.DoesNotExist:
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
        return token.key, user

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
            DishInOrder.objects.create(
                to_order=order, dish=Dish.objects.get(id=dish_id))

    @database_sync_to_async
    def get_order_info(self, order_id):
        data = DishInOrder.objects.filter(to_order=order_id)
        serializer = DishInOrderSerializer(data, many=True)
        json_data = serializer.data
        return json_data

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
    def form_tables_data(self):
        data = Table.objects.all()
        serializer = TableSerializer(data, many=True)
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
        self.custom_user = await self.get_custom_user_from_user(self.user)
        if self.user:
            await self.accept()
            await self.send(text_data=json.dumps({"action": "GET_ROLE_RESPONSE", "data": self.custom_user.role}))
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
            token, new_user = await self.get_token_new_role(role)
            await self.send(text_data=json.dumps({"action": "NEW_ROLE_RESPONSE",
                                                  "data": {
                                                      "token": token,
                                                      "role": new_user.role},
                                                  }, ensure_ascii=False))
        elif action == 'NEW_ROLE' and role not in (1, 2):
            await self.send(text_data=json.dumps({"action": "NEW_ROLE_RESPONSE", "data": "Неверная роль."}, ensure_ascii=False))

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
            await self.send(text_data=json.dumps({'action': 'ENTER_NAME_RESPONSE', 'data': 'Данные были обновлены.'}, ensure_ascii=False))

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


        # взять на себя обслуживание столика
        """
        {
            "action": "I_SERVE",
            "data": 4
        }
        """
        if action == "I_SERVE":
            await self.perform_i_serve(data.get("data"))
            await self.send(text_data=json.dumps({"action": "I_SERVE_RESPONSE", "data": "Официант взял столик."}, ensure_ascii=False))

        # просмотреть все меню
        """
        {
            "action": "SHOW_MENU"
        }
        """
        if action == "SHOW_MENU":
            temp_data = await self.form_menu_data()
            await self.send(text_data=json.dumps({"action": "SHOW_MENU_RESPONSE", "data": temp_data}, ensure_ascii=False))

        # просмотреть все столики
        """
        {
            "action": "SHOW_TABLES"
        }
        """
        if action == "SHOW_TABLES":
            temp_data = await self.form_tables_data()
            await self.send(text_data=json.dumps({"action": "SHOW_TABLES_RESPONSE", "data": temp_data}, ensure_ascii=False))

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
            await self.send(text_data=json.dumps({"action": "MAKE_ORDER_RESPONSE", "data": "Заказ создан."}, ensure_ascii=False))

        # получить список всех пользователей, если ты администратор
        """
        {
            "action": "GET_USERS"
        }
        """
        if action == "GET_USERS":
            temp_data = await self.get_users_data()
            await self.send(text_data=json.dumps({"action": "GET_USERS_RESPONSE", "data": temp_data}, ensure_ascii=False))

        # получить данные о готовке и блюдах в заказе
        """
        {
            "action": "ORDER_INFO",
            "data": 4
        }
        """
        if action == "ORDER_INFO":
            order_id = data.get("data")
            temp_data = await self.get_order_info(order_id)
            await self.send(text_data=json.dumps({"action": "ORDER_INFO_RESPONSE", "data": temp_data}, ensure_ascii=False))

        # изменить статус готовки блюда
        """
        {
            "action": "UPDATE_ORDER",
            "data": {
                "table_id": 4,
                "order": [
                    {
                        "dish_in_order_id": 7
                        "new_status": 2
                    },
                    {
                        "dish_in_order_id": 8
                        "new_status": 3
                    },
                    {
                        "dish_in_order_id": 9
                        "new_status": 3
                    },
                    {
                        "dish_in_order_id": 10
                        "new_status": 4
                    }
                ]
            }
        }
        """
        if action == "UPDATE_ORDER":
            temp_data = data.get("data")
            table_id = temp_data["table_id"]
            order_from_request = temp_data["order"]
