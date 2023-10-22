from rest_framework import serializers
from django.contrib.auth.models import User
from.models import CustomUser, Dish

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'role', 'user')

class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ("title", "description", "link_to_photo")
