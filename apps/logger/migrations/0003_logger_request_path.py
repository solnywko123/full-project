# Generated by Django 4.2.7 on 2023-11-24 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logger', '0002_rename_requests_data_logger_request_data_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='logger',
            name='request_path',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
