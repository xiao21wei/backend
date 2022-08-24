# Generated by Django 4.0.6 on 2022-08-10 03:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('code', models.CharField(blank=True, max_length=10, null=True)),
                ('mail', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('send_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'code',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Element',
            fields=[
                ('prototype_id', models.IntegerField(blank=True, null=True)),
                ('custom_id', models.IntegerField(primary_key=True, serialize=False)),
                ('width', models.IntegerField(blank=True, null=True)),
                ('height', models.IntegerField(blank=True, null=True)),
                ('x', models.IntegerField(blank=True, null=True)),
                ('y', models.IntegerField(blank=True, null=True)),
                ('element_type', models.CharField(blank=True, max_length=20, null=True)),
                ('rotation', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'element',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('folder_id', models.AutoField(primary_key=True, serialize=False)),
                ('team_id', models.IntegerField()),
                ('folder_name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'folder',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='OtherDocument',
            fields=[
                ('document_id', models.AutoField(primary_key=True, serialize=False)),
                ('room_name', models.CharField(max_length=255, unique=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'other_document',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('project_id', models.AutoField(primary_key=True, serialize=False)),
                ('project_name', models.CharField(blank=True, max_length=50, null=True)),
                ('introduction', models.CharField(blank=True, max_length=255, null=True)),
                ('recycle', models.IntegerField(blank=True, null=True)),
                ('create_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'project',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProjectDocument',
            fields=[
                ('document_id', models.AutoField(primary_key=True, serialize=False)),
                ('room_name', models.CharField(max_length=255, unique=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'project_document',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Prototype',
            fields=[
                ('project_id', models.IntegerField(blank=True, null=True)),
                ('prototype_id', models.IntegerField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'prototype',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('room_id', models.AutoField(primary_key=True, serialize=False)),
                ('room_name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'db_table': 'room',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('team_id', models.AutoField(primary_key=True, serialize=False)),
                ('team_name', models.CharField(blank=True, max_length=50, null=True)),
                ('introduction', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'team',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.JSONField(blank=True, null=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'test',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Uml',
            fields=[
                ('uml_id', models.IntegerField(db_column='UML_id', primary_key=True, serialize=False)),
                ('picture', models.CharField(blank=True, max_length=255, null=True)),
                ('author', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'UML',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_id', models.IntegerField(blank=True, null=True)),
                ('user_id', models.IntegerField(blank=True, null=True)),
                ('user_identity', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'db_table': 'user_team',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserUser',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'user_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserWebUser',
            fields=[
                ('status', models.CharField(max_length=50)),
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=50, unique=True)),
                ('real_name', models.CharField(blank=True, max_length=50, null=True)),
                ('pass_word', models.CharField(max_length=50)),
                ('mail', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('phone', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'user_web_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TeamProject',
            fields=[
                ('project', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='user_web.project')),
            ],
            options={
                'db_table': 'team_project',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserProject',
            fields=[
                ('project', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='user_web.project')),
            ],
            options={
                'db_table': 'user_project',
                'managed': False,
            },
        ),
    ]