from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CustomUser, Dish


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
        fields = ("title", "description", "link_to_photo")
