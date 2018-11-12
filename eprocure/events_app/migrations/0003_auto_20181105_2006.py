# Generated by Django 2.0.5 on 2018-11-05 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events_app', '0002_auto_20181105_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='children_count',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='group',
            name='speculated_venue',
            field=models.CharField(blank=True, default='Nairobi', max_length=1000),
        ),
        migrations.AlterField(
            model_name='group',
            name='start_time',
            field=models.TimeField(blank=True, default='10:00'),
        ),
    ]
