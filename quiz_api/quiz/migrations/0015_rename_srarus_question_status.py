# Generated by Django 3.2.9 on 2022-04-07 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0014_auto_20220407_1259'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='srarus',
            new_name='status',
        ),
    ]
