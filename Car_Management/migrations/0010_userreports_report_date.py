# Generated by Django 5.0.2 on 2024-06-14 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Car_Management', '0009_alter_usercars_car_image_alter_userreports_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='userreports',
            name='report_date',
            field=models.DateField(),
        ),
    ]