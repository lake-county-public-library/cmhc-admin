# Generated by Django 3.1.5 on 2021-01-23 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stage', '0002_remove_status_msg'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='csv_staged',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='status',
            name='deploy_aws',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='status',
            name='deploy_local',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='status',
            name='derivatives_generated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='status',
            name='images_staged',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='status',
            name='indexes_rebuilt',
            field=models.BooleanField(default=False),
        ),
    ]
