# Generated by Django 5.0 on 2024-09-22 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='comment',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Комментарий для курьера'),
        ),
    ]
