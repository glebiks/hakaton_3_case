from django.contrib import admin
from .models import CustomUser, Order, Table, Dish

# Административный класс для модели CustomUser
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')

# Административный класс для модели Order
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'dish', 'cooker', 'status')

# Административный класс для модели Dish
class DishAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')

# Административный класс для модели Table
class TableAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'order', 'waiter')

# Регистрация административных классов
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Dish, DishAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Table, TableAdmin)



