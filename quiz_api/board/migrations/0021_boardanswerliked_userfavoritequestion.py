# Generated by Django 3.2.9 on 2022-03-21 02:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_thumbnail'),
        ('board', '0020_auto_20220314_1028'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFavoriteQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked_num', models.IntegerField(default=0)),
                ('question', models.ManyToManyField(related_name='favorite_question', to='board.BoardQuestion')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='favorite_question', to='user.user')),
            ],
        ),
        
    ]
