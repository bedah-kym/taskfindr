# Generated by Django 4.0.4 on 2024-11-02 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_profile_is_verified_profile_work_done'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='preference',
        ),
        migrations.AddField(
            model_name='profile',
            name='otp',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(default=' '),
        ),
    ]
