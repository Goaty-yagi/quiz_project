# Generated by Django 3.2.9 on 2022-04-07 11:20

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0010_alter_question_correct_answer'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParentField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ParentQuiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ParentStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='question',
            name='module',
        ),
        migrations.RemoveField(
            model_name='question',
            name='order',
        ),
        migrations.RemoveField(
            model_name='quiztaker',
            name='timestamp',
        ),
        migrations.AddField(
            model_name='answer',
            name='taken_num',
            field=models.IntegerField(default=0),
        ),
        migrations.RemoveField(
            model_name='question',
            name='field',
        ),
        migrations.AlterField(
            model_name='quiz',
            name='slug',
            field=models.SlugField(default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='question_type',
            field=models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.questiontype'),
        ),
        migrations.AddField(
            model_name='question',
            name='srarus',
            field=models.ManyToManyField(blank=True, to='quiz.ParentStatus'),
        ),
        migrations.AddField(
            model_name='question',
            name='field',
            field=models.ManyToManyField(to='quiz.ParentField'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.parentquiz'),
        ),
    ]
