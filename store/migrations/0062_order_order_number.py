# Generated by Django 5.1.6 on 2025-02-20 17:37

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0061_remove_order_cart_number_alter_order_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_number',
            field=models.CharField(default=uuid.uuid4, max_length=100, unique=True),
        ),
    ]
