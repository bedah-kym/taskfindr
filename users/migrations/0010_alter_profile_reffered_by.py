# Generated by Django 4.0.4 on 2023-05-01 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_profile_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='reffered_by',
            field=models.CharField(default=None, max_length=50, null=True),
        ),
    ]
