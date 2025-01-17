# Generated by Django 4.2.7 on 2024-04-15 10:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name_uz', models.CharField(max_length=255)),
                ('name_ru', models.CharField(blank=True, max_length=255, null=True)),
                ('name_en', models.CharField(blank=True, max_length=255, null=True)),
                ('username', models.CharField(db_index=True, max_length=100, unique=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('children', models.ManyToManyField(blank=True, related_name='children', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_type', models.CharField(choices=[('Personal', 'Personal'), ('Group', 'Group')], max_length=20)),
                ('participant', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Conversation',
                'verbose_name_plural': 'Conversations',
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.SmallIntegerField()),
                ('type', models.CharField(choices=[('a', 'a'), ('б', 'б'), ('в', 'в'), ('г', 'г'), ('д', 'д')], max_length=1)),
                ('teacher', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='class_teacher', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Class',
                'verbose_name_plural': 'Classes',
                'unique_together': {('number', 'type')},
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_uz', models.CharField(max_length=255)),
                ('name_ru', models.CharField(blank=True, max_length=255, null=True)),
                ('name_en', models.CharField(blank=True, max_length=255, null=True)),
                ('user_type', models.CharField(choices=[('Teacher', 'Teacher'), ('Student', 'Student'), ('Parent', 'Parent')], default='Student', max_length=7)),
            ],
            options={
                'verbose_name': 'Role',
                'verbose_name_plural': 'Roles',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_uz', models.CharField(max_length=255)),
                ('name_ru', models.CharField(blank=True, max_length=255, null=True)),
                ('name_en', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Subject',
                'verbose_name_plural': 'Subjects',
            },
        ),
        migrations.CreateModel(
            name='SubjectTeacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject_teacher_class', to='configs.grade')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject_teacher_subject', to='configs.subject')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject_teacher_teacher', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Subject-Teacher',
                'verbose_name_plural': 'Subjects-Teachers',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(default='default-text', max_length=255)),
                ('is_changed', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('Sent', 'Sent'), ('Seen', 'Seen')], default='Sent', max_length=10)),
                ('viewed_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('conversation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='configs.conversation')),
                ('reply_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='configs.message')),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
        ),
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deadline', models.DateTimeField()),
                ('mark', models.PositiveSmallIntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True)),
                ('task_file', models.FileField(upload_to='homework_tasks/')),
                ('student_answer', models.FileField(blank=True, null=True, upload_to='student_answers/')),
                ('status', models.CharField(choices=[('Assigned', 'Assigned'), ('Submitted', 'Submitted'), ('Marked', 'Marked')], default='assigned', max_length=10)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_homeworks', to=settings.AUTH_USER_MODEL)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='set_homeworks', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Homework',
                'verbose_name_plural': 'Homeworks',
            },
        ),
        migrations.CreateModel(
            name='DairyOfClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('quarter', models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4)])),
                ('grade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dairy_of_class', to='configs.grade')),
                ('pupil', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dairy_pupil', to=settings.AUTH_USER_MODEL)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject', to='configs.subject')),
            ],
            options={
                'verbose_name': 'DairyOfClass',
                'verbose_name_plural': 'DairiesOfClass_class',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='grade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_grade', to='configs.grade'),
        ),
        migrations.AddField(
            model_name='user',
            name='parent',
            field=models.ManyToManyField(blank=True, related_name='parent', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='configs.role'),
        ),
    ]
