# Generated by Django 5.0.7 on 2024-08-19 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0003_remove_feedback_telegram_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]
