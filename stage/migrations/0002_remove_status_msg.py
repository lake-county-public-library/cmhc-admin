# Generated by Django 3.1.5 on 2021-01-07 16:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stage', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='status',
            name='msg',
        ),
    ]
