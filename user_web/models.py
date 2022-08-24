# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


# class AuthGroup(models.Model):
#     name = models.CharField(unique=True, max_length=150)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_group'
#
#
# class AuthGroupPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#     permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_group_permissions'
#         unique_together = (('group', 'permission'),)
#
#
# class AuthPermission(models.Model):
#     name = models.CharField(max_length=255)
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
#     codename = models.CharField(max_length=100)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_permission'
#         unique_together = (('content_type', 'codename'),)
#
#
# class AuthUser(models.Model):
#     password = models.CharField(max_length=128)
#     last_login = models.DateTimeField(blank=True, null=True)
#     is_superuser = models.IntegerField()
#     username = models.CharField(unique=True, max_length=150)
#     first_name = models.CharField(max_length=150)
#     last_name = models.CharField(max_length=150)
#     email = models.CharField(max_length=254)
#     is_staff = models.IntegerField()
#     is_active = models.IntegerField()
#     date_joined = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'auth_user'
#
#
# class AuthUserGroups(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_user_groups'
#         unique_together = (('user', 'group'),)
#
#
# class AuthUserUserPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_user_user_permissions'
#         unique_together = (('user', 'permission'),)


class Code(models.Model):
    mail = models.CharField(primary_key=True, max_length=50)
    code = models.CharField(max_length=10, blank=True, null=True)
    send_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'code'


# class DjangoAdminLog(models.Model):
#     action_time = models.DateTimeField()
#     object_id = models.TextField(blank=True, null=True)
#     object_repr = models.CharField(max_length=200)
#     action_flag = models.PositiveSmallIntegerField()
#     change_message = models.TextField()
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = 'django_admin_log'
#
#
# class DjangoContentType(models.Model):
#     app_label = models.CharField(max_length=100)
#     model = models.CharField(max_length=100)
#
#     class Meta:
#         managed = False
#         db_table = 'django_content_type'
#         unique_together = (('app_label', 'model'),)
#
#
# class DjangoMigrations(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     app = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     applied = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'django_migrations'
#
#
# class DjangoSession(models.Model):
#     session_key = models.CharField(primary_key=True, max_length=40)
#     session_data = models.TextField()
#     expire_date = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'django_session'
#
#
# class Document(models.Model):
#     document_id = models.AutoField(primary_key=True)
#     title = models.CharField(max_length=50, blank=True, null=True)
#     content = models.TextField(blank=True, null=True)
#     author = models.CharField(max_length=50, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'document'


class Element(models.Model):
    prototype_id = models.IntegerField(blank=True, null=True)
    custom_id = models.DateField(primary_key=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    x = models.IntegerField(blank=True, null=True)
    y = models.IntegerField(blank=True, null=True)
    element_type = models.CharField(max_length=20, blank=True, null=True)
    rotation = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'element'


class Folder(models.Model):
    folder_id = models.AutoField(primary_key=True)
    team_id = models.IntegerField()
    folder_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'folder'


class OtherDocument(models.Model):
    document_id = models.AutoField(primary_key=True)
    folder = models.ForeignKey(Folder, models.DO_NOTHING)
    room_name = models.CharField(unique=True, max_length=255, db_collation='utf8mb4_0900_ai_ci', blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.JSONField(blank=True, null=True)
    open_type = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'other_document'


class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=50, blank=True, null=True)
    introduction = models.CharField(max_length=255, blank=True, null=True)
    recycle = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project'


class ProjectDocument(models.Model):
    document_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, models.DO_NOTHING)
    room_name = models.CharField(unique=True, max_length=255, db_collation='utf8mb4_0900_ai_ci')
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.JSONField(blank=True, null=True)
    open_type = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project_document'


class Prototype(models.Model):
    project_id = models.IntegerField(blank=True, null=True)
    prototype_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'prototype'


class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_name = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'room'


class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=50, blank=True, null=True)
    introduction = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'team'


class TeamProject(models.Model):
    team = models.ForeignKey(Team, models.DO_NOTHING)
    project = models.OneToOneField(Project, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'team_project'


class Test(models.Model):
    content = models.JSONField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    project = models.ForeignKey(Project, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test'


class Test1(models.Model):
    content = models.JSONField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    project = models.ForeignKey(Project, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test1'


class UserWebUser(models.Model):
    status = models.CharField(max_length=50)
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(unique=True, max_length=50)
    real_name = models.CharField(max_length=50, blank=True, null=True)
    pass_word = models.CharField(max_length=50)
    mail = models.CharField(unique=True, max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'user_web_user'
