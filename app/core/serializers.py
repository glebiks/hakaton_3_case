from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CustomUser, Dish, DishInOrder, Table



class TableSerializer(serializers.ModelSerializer):
    waiter_name = serializers.SerializerMethodField()

    class Meta:
        model = Table
        fields = ('id', 'status', 'order', 'waiter', 'waiter_name')

    def get_waiter_name(self, obj):
        return obj.waiter.username

class CustomUserSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'role', 'user', 'user_name', 'rate_count', 'rate_sum')

    def get_user_name(self, obj):
        return obj.user.username


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ("id", "title", "description", "link_to_photo")

class DishInOrderSerializer(serializers.ModelSerializer):
    dish_title = serializers.SerializerMethodField()

    class Meta:
        model = DishInOrder
        fields = ("id", "dish_title", "status", "to_order")

    def get_dish_title(self, obj):
        return obj.dish.title
