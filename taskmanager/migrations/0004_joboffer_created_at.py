# Generated by Django 4.0.4 on 2024-10-17 22:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0003_alter_joboffer_bids_alter_joboffer_milestones'),
    ]

    operations = [
        migrations.AddField(
            model_name='joboffer',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
