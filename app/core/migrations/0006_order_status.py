# Generated by Django 4.1 on 2023-10-21 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_table_order_alter_table_waiter'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(1, 'Ожидает'), (2, 'Готовится'), (3, 'Готово'), (4, 'Выдано')], default=1, verbose_name='status'),
        ),
    ]
