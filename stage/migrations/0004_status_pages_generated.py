# Generated by Django 3.1.5 on 2021-01-24 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stage', '0003_auto_20210123_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='pages_generated',
            field=models.BooleanField(default=False),
        ),
    ]
