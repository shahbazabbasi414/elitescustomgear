# Generated by Django 5.0.6 on 2024-10-10 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0031_rename_customization_customization_customization_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='color',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='order',
            name='customization',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='order',
            name='gsm',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='order',
            name='material',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='order',
            name='size',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='order',
            name='type',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
