# Generated by Django 5.0.6 on 2024-10-09 19:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0029_rename_color_color_color'),
    ]

    operations = [
        migrations.RenameField(
            model_name='type',
            old_name='Type',
            new_name='type',
        ),
    ]
