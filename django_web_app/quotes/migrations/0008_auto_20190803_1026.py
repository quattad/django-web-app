# Generated by Django 2.2.3 on 2019-08-03 02:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0007_auto_20190730_2313'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quote',
            name='user_favourited',
        ),
        migrations.RemoveField(
            model_name='quote',
            name='user_liked',
        ),
    ]
