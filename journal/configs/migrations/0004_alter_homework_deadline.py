# Generated by Django 4.2.7 on 2024-04-18 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configs', '0003_alter_dairyofclass_options_alter_homework_deadline_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homework',
            name='deadline',
            field=models.DateTimeField(),
        ),
    ]