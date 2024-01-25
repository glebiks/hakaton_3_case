from django.db import models
from django.contrib.auth.models import User


class CustomUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.IntegerField(
        verbose_name='Role', choices=((1, 'cooker'), (2, 'waiter')))
    rate_count = models.IntegerField(default=0)
    rate_sum = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Dish(models.Model):
    title = models.CharField(max_length=128, blank=False)
    description = models.TextField(blank=True)
    cooker = models.ForeignKey(User, on_delete=models.CASCADE, default=5)
    link_to_photo = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.title


class Order(models.Model):

    def __str__(self):
        return str(self.id)


class DishInOrder(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, default=1)
    STATUSES = (
        (1, "Ожидает"),
        (2, "Готовится"),
        (3, "Готово"),
        (4, "Выдано"),
    )
    status = models.IntegerField(
        verbose_name="status", choices=STATUSES, default=1)
    to_order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return self.dish.title


class Table(models.Model):
    STATUSES = (
        (1, "Свободен"),
        (2, "Забронирован"),
        (3, "Занят (ожидает заказа)"),
        (4, "Занят (заказано)"),
        (5, "Занят (обслужен)"),
        (6, "Свободен (ожидает уборки)"),
    )
    status = models.IntegerField(verbose_name="table_status", choices=STATUSES)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, null=True, blank=True)
    waiter = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.id)
