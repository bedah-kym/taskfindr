# Generated by Django 4.0.4 on 2024-10-16 21:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0022_blogpost_assigned_to_blogpost_is_closed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='value',
        ),
    ]
