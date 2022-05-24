# Generated by Django 3.2.8 on 2022-05-17 10:04

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExtraData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField()),
                ('name', models.CharField(max_length=100)),
                ('comments', models.TextField()),
            ],
            options={
                'db_table': 'extra_data',
            },
        ),
        migrations.CreateModel(
            name='FormatContentModel',
            fields=[
                ('id', models.BigAutoField(db_column='id_format_content', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='format_name', max_length=100)),
            ],
            options={
                'db_table': 'format_content',
            },
        ),
        migrations.CreateModel(
            name='MetricsNameModel',
            fields=[
                ('id', models.BigAutoField(db_column='id_metrics_name', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='metrics_name', max_length=150)),
            ],
            options={
                'db_table': 'metrics_name',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField()),
                ('priority', models.IntegerField()),
                ('fields', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), size=None)),
            ],
            options={
                'db_table': 'task',
            },
        ),
        migrations.CreateModel(
            name='TaskStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'task_status',
            },
        ),
        migrations.CreateModel(
            name='TaskType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'task_type',
            },
        ),
        migrations.CreateModel(
            name='TypeFields',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fields', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), size=None)),
                ('task_type', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='type_fields', to='main.tasktype')),
            ],
            options={
                'db_table': 'task_type_fields',
            },
        ),
        migrations.CreateModel(
            name='TaskResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.FileField(upload_to='')),
                ('comment', models.TextField(null=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.task')),
            ],
            options={
                'db_table': 'task_result',
            },
        ),
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.taskstatus'),
        ),
        migrations.AddField(
            model_name='task',
            name='task_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.tasktype'),
        ),
    ]
