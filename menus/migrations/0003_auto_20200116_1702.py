# Generated by Django 3.0.2 on 2020-01-16 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0003_auto_20200111_2154'),
        ('menus', '0002_menu_restaurant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menus', to='restaurants.Restaurant'),
        ),
    ]
