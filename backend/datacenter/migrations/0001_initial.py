# Generated by Django 5.0 on 2024-09-22 09:37

import django.db.models.deletion
import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('value_from', models.FloatField(verbose_name='Сумма от')),
                ('value_to', models.FloatField(verbose_name='Сумма до')),
            ],
            options={
                'verbose_name': 'Бюджет',
                'verbose_name_plural': 'Бюджеты',
            },
        ),
        migrations.CreateModel(
            name='Bunch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название букета')),
                ('price', models.FloatField(verbose_name='Цена букета')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Изображение букета')),
                ('caption', models.TextField(blank=True, null=True, verbose_name='Описание букета')),
            ],
            options={
                'verbose_name': 'Букет',
                'verbose_name_plural': 'Букеты',
            },
        ),
        migrations.CreateModel(
            name='BunchElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название элемента букета')),
            ],
            options={
                'verbose_name': 'Элемент букета',
                'verbose_name_plural': 'Элементы букета',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_tg', models.IntegerField(blank=True, null=True, unique=True, verbose_name='id в телеграмм')),
                ('full_name', models.CharField(max_length=200, verbose_name='ФИО')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region='RU', verbose_name='Номер телефона')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
        migrations.CreateModel(
            name='Motive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Повод')),
            ],
            options={
                'verbose_name': 'Повод',
                'verbose_name_plural': 'Поводы',
            },
        ),
        migrations.CreateModel(
            name='BunchAssembly',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1, verbose_name='Количество')),
                ('bunch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='datacenter.bunch', verbose_name='Букет')),
                ('element', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='datacenter.bunchelement', verbose_name='Элемент букета')),
            ],
            options={
                'verbose_name': 'Элемент букета',
                'verbose_name_plural': 'Элементы букета',
            },
        ),
        migrations.AddField(
            model_name='bunch',
            name='elements',
            field=models.ManyToManyField(related_name='bunch', through='datacenter.BunchAssembly', to='datacenter.bunchelement', verbose_name='Элементы букета'),
        ),
        migrations.AddField(
            model_name='bunch',
            name='motive',
            field=models.ManyToManyField(related_name='bunch', to='datacenter.motive', verbose_name='Повод'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('accepted', 'Принят'), ('confirmed', 'Подтвержден'), ('completed', 'Выполнен'), ('canceled', 'Отменен')], default='accepted', max_length=9, verbose_name='Статус заказа')),
                ('date', models.DateField(auto_now_add=True, verbose_name='Дата заказа')),
                ('time', models.TimeField(auto_now_add=True, verbose_name='Время заказа')),
                ('delivery_date', models.DateField(verbose_name='Дата доставки')),
                ('delivery_time', models.TimeField(verbose_name='Время доставки')),
                ('delivery_address', models.TextField(blank=True, max_length=200, null=True, verbose_name='Адрес доставки')),
                ('bunch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='datacenter.bunch', verbose_name='Букет')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='datacenter.client', verbose_name='Клиент')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
    ]
