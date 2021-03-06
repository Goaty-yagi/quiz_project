# Generated by Django 3.2.9 on 2021-11-21 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0006_auto_20211109_0608'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='correct_answer',
            field=models.JSONField(default='[]'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
