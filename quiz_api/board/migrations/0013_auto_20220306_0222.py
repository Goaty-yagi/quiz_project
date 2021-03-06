# Generated by Django 3.2.9 on 2022-03-06 02:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_thumbnail'),
        ('board', '0012_auto_20220306_0214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boardcentertag',
            name='question',
            field=models.ManyToManyField(blank=True, default=None, related_name='cnter_tag', to='board.BoardQuestion'),
        ),
        migrations.AlterField(
            model_name='boardcentertag',
            name='user',
            field=models.ManyToManyField(blank=True, default=None, related_name='cnter_tag', to='user.User'),
        ),
        migrations.RemoveField(
            model_name='boardusertag',
            name='tag',
        ),
        migrations.AddField(
            model_name='boardusertag',
            name='tag',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='board.boardcentertag'),
        ),
        migrations.RemoveField(
            model_name='boardusertag',
            name='user',
        ),
        migrations.AddField(
            model_name='boardusertag',
            name='user',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='user_tag', to='user.user'),
        ),
    ]
