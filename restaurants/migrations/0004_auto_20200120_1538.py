# Generated by Django 3.0.2 on 2020-01-20 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0003_auto_20200111_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='payment_method',
            field=models.ManyToManyField(to='restaurants.PaymentMethod'),
        ),
    ]
