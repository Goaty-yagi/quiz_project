# Generated by Django 3.2.9 on 2022-07-05 06:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0003_rename_checke_logger_checked'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='logger',
            options={'ordering': ['-created_on']},
        ),
    ]
