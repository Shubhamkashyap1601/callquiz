# Generated by Django 5.1.4 on 2025-01-03 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_quiz_time_limit_quizresult'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='option_1',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='question',
            name='option_2',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='question',
            name='option_3',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='question',
            name='option_4',
            field=models.CharField(default='', max_length=255),
        ),
    ]
