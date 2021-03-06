# Generated by Django 3.2.9 on 2022-04-20 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0018_rename_level_question_quiz_level'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_correct', models.BooleanField(default=False)),
                ('is_false', models.BooleanField(default=False)),
                ('percentage', models.IntegerField(default=0)),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.parentquiz')),
            ],
        ),
        migrations.RenameField(
            model_name='quiztaker',
            old_name='score',
            new_name='level',
        ),
        migrations.RemoveField(
            model_name='quiztaker',
            name='completed',
        ),
        migrations.RemoveField(
            model_name='quiztaker',
            name='quiz',
        ),
        migrations.AddField(
            model_name='parentstatus',
            name='grade',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='quiz.parentfield'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quiztaker',
            name='grade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.parentquiz'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quiztaker',
            name='quiz_practice_num',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='quiztaker',
            name='test_take_num',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='UsersAnswer',
        ),
        migrations.AddField(
            model_name='userstatus',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.parentstatus'),
        ),
        migrations.AddField(
            model_name='quiztaker',
            name='user_status',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='quiz.userstatus'),
            preserve_default=False,
        ),
    ]
