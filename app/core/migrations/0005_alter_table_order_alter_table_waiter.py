# Generated by Django 4.1 on 2023-10-21 22:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0004_dish_remove_order_description_remove_order_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.order'),
        ),
        migrations.AlterField(
            model_name='table',
            name='waiter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
