# Generated by Django 4.1 on 2023-10-21 23:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0008_remove_order_cooker_dish_cooker'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='dish',
        ),
        migrations.AlterField(
            model_name='dish',
            name='cooker',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
