# Generated by Django 5.1.3 on 2024-12-19 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_user_email_userperformance'),
    ]

    operations = [
        migrations.AddField(
            model_name='userperformance',
            name='exam_type',
            field=models.CharField(choices=[('single_subject', 'Single Subject'), ('complete_mock', 'Complete Mock Exam')], default='single_subject', max_length=20),
        ),
    ]
