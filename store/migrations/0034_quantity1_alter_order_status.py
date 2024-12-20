# Generated by Django 5.0.6 on 2024-12-09 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0033_alter_order_color_alter_order_customization_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quantity1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Designing & Quotation', 'Designing & Quotation'), ('Pending Customer Approval', 'Pending Customer Approval'), ('Order Under Production', 'Order Under Production'), ('Dispatched', 'Dispatched'), ('Delivered', 'Delivered')], default='Designing & Quotation', max_length=50),
        ),
    ]