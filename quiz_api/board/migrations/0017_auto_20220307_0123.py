# Generated by Django 3.2.9 on 2022-03-07 01:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_thumbnail'),
        ('board', '0016_auto_20220307_0046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boardcentertag',
            name='question',
        ),
        migrations.RemoveField(
            model_name='boardquestion',
            name='tag',
        ),
        migrations.AddField(
            model_name='boardquestion',
            name='tag',
            field=models.ManyToManyField(related_name='question', to='board.BoardCenterTag'),
        ),
        
    ]
