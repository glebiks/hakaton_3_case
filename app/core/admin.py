from django.contrib import admin
from .models import CustomUser, Order, Table, Dish, DishInOrder

# Административный класс для модели CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'role', 'rate_count', 'rate_sum')

# Административный класс для модели Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id',)

# Административный класс для модели Dish


class DishAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'link_to_photo', 'cooker')

# Административный класс для модели DishInOrder


class DishInOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'dish', 'to_order', 'status')

# Административный класс для модели Table


class TableAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'order', 'waiter')


# Регистрация административных классов
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Dish, DishAdmin)
admin.site.register(DishInOrder, DishInOrderAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Table, TableAdmin)
