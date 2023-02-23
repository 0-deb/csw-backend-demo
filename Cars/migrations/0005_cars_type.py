# Generated by Django 4.1.6 on 2023-02-15 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cars', '0004_alter_cars_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='cars',
            name='type',
            field=models.CharField(choices=[('Petrol', 'Petrol'), ('Diesel', 'Diesel'), ('CNG', 'CNG')], default='Petrol', max_length=255),
            preserve_default=False,
        ),
    ]
