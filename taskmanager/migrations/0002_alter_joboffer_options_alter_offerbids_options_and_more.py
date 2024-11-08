# Generated by Django 4.0.4 on 2024-10-16 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='joboffer',
            options={'verbose_name': 'job offers', 'verbose_name_plural': 'job offers'},
        ),
        migrations.AlterModelOptions(
            name='offerbids',
            options={'verbose_name': 'offer bids', 'verbose_name_plural': 'offer bids'},
        ),
        migrations.AlterModelOptions(
            name='offermilestones',
            options={'verbose_name': 'offer milestones', 'verbose_name_plural': 'offer milestones'},
        ),
        migrations.AlterField(
            model_name='joboffer',
            name='bids',
            field=models.ManyToManyField(default=None, null=True, related_name='job_bids', to='taskmanager.offerbids'),
        ),
        migrations.AlterField(
            model_name='joboffer',
            name='milestones',
            field=models.ManyToManyField(default=None, null=True, related_name='job_milestones', to='taskmanager.offermilestones'),
        ),
    ]
