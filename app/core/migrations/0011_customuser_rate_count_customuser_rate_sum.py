# Generated by Django 4.1 on 2023-10-22 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_dish_link_to_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='rate_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='customuser',
            name='rate_sum',
            field=models.IntegerField(default=0),
        ),
    ]
