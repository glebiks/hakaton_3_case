# Generated by Django 4.1 on 2023-10-22 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_remove_order_dish_alter_dish_cooker'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='link_to_photo',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
