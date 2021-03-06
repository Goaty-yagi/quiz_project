# Generated by Django 3.2.9 on 2022-03-06 01:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_thumbnail'),
        ('board', '0010_boardquestionliked'),
    ]

    operations = [
        migrations.CreateModel(
            name='BoardCenterTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=200)),
                ('used_num', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='BoardParentCenterTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent_tag', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='boardquestionliked',
            name='answer',
        ),
        migrations.CreateModel(
            name='BoardUserTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('used_num', models.IntegerField(default=0)),
                ('tag', models.ManyToManyField(to='board.BoardCenterTag')),
                ('user', models.ManyToManyField(default=None, related_name='user_tag', to='user.User')),
            ],
        ),
        migrations.AddField(
            model_name='boardcentertag',
            name='parent_tag',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cnter_tag', to='board.boardparentcentertag'),
        ),
        migrations.AddField(
            model_name='boardcentertag',
            name='question',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='board.boardquestion'),
        ),
        migrations.AddField(
            model_name='boardcentertag',
            name='user',
            field=models.ManyToManyField(to='user.User'),
        ),
    ]
