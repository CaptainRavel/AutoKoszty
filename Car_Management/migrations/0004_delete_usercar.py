# Generated by Django 5.0.2 on 2024-06-13 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Car_Management', '0003_usercar_usercars'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserCar',
        ),
    ]