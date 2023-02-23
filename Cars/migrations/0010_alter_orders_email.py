# Generated by Django 4.1.6 on 2023-02-22 09:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cars', '0009_alter_orders_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='email',
            field=models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(message='Invalid email format', regex='[a-z0-9]{3,}\\@[a-z0-9]{2,}\\.[a-z]{2,}')]),
        ),
    ]
