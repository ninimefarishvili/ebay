# Generated by Django 5.1.2 on 2024-12-17 08:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0014_alter_cart_created_at_alter_product_listing_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 17, 8, 30, 27, 875957, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='product',
            name='listing_date',
            field=models.DateField(default=datetime.datetime(2024, 12, 17, 8, 30, 27, 874958, tzinfo=datetime.timezone.utc)),
        ),
    ]
