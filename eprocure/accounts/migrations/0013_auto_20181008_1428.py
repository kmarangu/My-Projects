# Generated by Django 2.0.5 on 2018-10-08 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20181008_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile_approved',
            name='approved',
            field=models.CharField(default='False', max_length=3, unique=True),
        ),
    ]