# Generated by Django 3.2.9 on 2022-02-02 06:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('board', '0003_delete_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='boardanswer',
            name='user',
            field=models.ForeignKey(default='none', on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='user.user'),
        ),
        migrations.AddField(
            model_name='boardquestion',
            name='user',
            field=models.ForeignKey(default='null', on_delete=django.db.models.deletion.CASCADE, related_name='question', to='user.user'),
        ),
    ]