# Generated by Django 4.0.4 on 2022-05-31 16:51

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0002_postinfo_author_postinfo_date_posted'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='postinfo',
            new_name='posts',
        ),
    ]
