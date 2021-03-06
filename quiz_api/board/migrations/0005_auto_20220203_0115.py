# Generated by Django 3.2.9 on 2022-02-03 01:15

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('board', '0004_auto_20220202_0629'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='boardanswer',
            options={'ordering': ['created_on']},
        ),
        migrations.AlterModelOptions(
            name='boardquestion',
            options={'ordering': ['created_on']},
        ),
        migrations.AlterModelOptions(
            name='boardreply',
            options={'ordering': ['created_on']},
        ),
        migrations.AlterModelOptions(
            name='boardreply2',
            options={'ordering': ['created_on']},
        ),
        migrations.RenameField(
            model_name='boardanswer',
            old_name='created_by',
            new_name='created_on',
        ),
        migrations.RenameField(
            model_name='boardquestion',
            old_name='created_by',
            new_name='created_on',
        ),
        migrations.RenameField(
            model_name='boardreply',
            old_name='created_by',
            new_name='created_on',
        ),
        migrations.RenameField(
            model_name='boardreply2',
            old_name='created_by',
            new_name='created_on',
        ),
        migrations.AlterField(
            model_name='boardanswer',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='user.user'),
        ),
        migrations.AlterField(
            model_name='boardquestion',
            name='slug',
            field=models.SlugField(default=uuid.UUID('26c53130-54ce-4ae9-9c13-bf0fa406b912')),
        ),
        migrations.AlterField(
            model_name='boardquestion',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='question', to='user.user'),
        ),
    ]
