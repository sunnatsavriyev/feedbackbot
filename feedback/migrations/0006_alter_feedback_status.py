# Generated by Django 5.0.7 on 2024-08-20 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0005_remove_feedback_is_read_feedback_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='status',
            field=models.CharField(choices=[('NEW', 'new'), ('DONE', 'done'), ('CANCEL', 'cancel')], default='NEW', max_length=9),
        ),
    ]
