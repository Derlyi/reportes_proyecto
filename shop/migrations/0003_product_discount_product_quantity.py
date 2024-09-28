# Generated by Django 5.1.1 on 2024-09-24 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
