# Generated by Django 4.0.4 on 2023-05-18 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_alter_cashaccount_mpesa_code_leveluprequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='leveled_up',
            field=models.BooleanField(default=False),
        ),
    ]
