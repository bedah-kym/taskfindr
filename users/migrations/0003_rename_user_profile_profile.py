# Generated by Django 4.0.4 on 2022-06-07 20:50

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0002_rename_profile_user_profile'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='user_Profile',
            new_name='profile',
        ),
    ]
