# Generated by Django 5.0.6 on 2025-02-18 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0053_customer_security_answer_1_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='security_answer_1',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='security_answer_2',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='security_answer_3',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='security_question_1',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='security_question_2',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='security_question_3',
        ),
    ]
