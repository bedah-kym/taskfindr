# Generated by Django 4.0.4 on 2024-10-13 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_jobrating_blogpost_rating_alter_blogpost_date_posted_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobrating',
            name='rating',
            field=models.IntegerField(choices=[]),
        ),
    ]
