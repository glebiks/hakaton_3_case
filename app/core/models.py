from django.db import models
from django.contrib.auth.models import User


class CustomUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.IntegerField(verbose_name='Role', choices=((1, 'cooker'), (2, 'waiter')))

    def __str__(self):
        return self.user.username
