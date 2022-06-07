# Generated by Django 3.2.9 on 2022-05-06 02:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20220430_0722'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='country',
        ),
        migrations.CreateModel(
            name='IPData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('ip', models.CharField(max_length=100)),
                ('loc', models.CharField(max_length=100)),
                ('org', models.CharField(max_length=100)),
                ('postal', models.CharField(max_length=100)),
                ('region', models.CharField(max_length=100)),
                ('timezone', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ip_data', to='user.user')),
            ],
        ),
    ]
