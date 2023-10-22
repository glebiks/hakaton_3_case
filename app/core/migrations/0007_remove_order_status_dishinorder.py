# Generated by Django 4.1 on 2023-10-21 23:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
        migrations.CreateModel(
            name='DishInOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, 'Ожидает'), (2, 'Готовится'), (3, 'Готово'), (4, 'Выдано')], default=1, verbose_name='status')),
                ('dish', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.dish')),
                ('to_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.order')),
            ],
        ),
    ]
