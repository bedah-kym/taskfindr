# Generated by Django 4.0.4 on 2024-10-12 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_jobrating_blogpost_rating_alter_blogpost_date_posted_and_more'),
        ('users', '0016_profile_leveled_up'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='work_done',
            field=models.ManyToManyField(related_name='jobs_done', to='blog.blogpost'),
        ),
    ]