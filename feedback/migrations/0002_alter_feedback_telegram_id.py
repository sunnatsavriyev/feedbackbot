# Generated by Django 5.0.7 on 2024-08-06 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='telegram_id',
            field=models.CharField(max_length=100),
        ),
    ]
