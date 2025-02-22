# Generated by Django 5.1.3 on 2025-01-15 14:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacollector', '0002_alter_pastquestion_correct_option'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subtopic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subtopics', to='datacollector.topic')),
            ],
        ),
    ]
