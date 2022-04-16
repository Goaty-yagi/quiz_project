# Generated by Django 3.2.9 on 2022-04-07 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0013_rename_srarus_question_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='status',
        ),
        migrations.RemoveField(
            model_name='quiztaker',
            name='timestamp',
        ),
        migrations.AddField(
            model_name='question',
            name='srarus',
            field=models.ManyToManyField(blank=True, to='quiz.ParentStatus'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='answer_id',
            field=models.IntegerField(default=0),
        ),
    ]