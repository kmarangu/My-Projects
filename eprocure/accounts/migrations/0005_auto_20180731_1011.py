# Generated by Django 2.0.2 on 2018-07-31 07:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20180731_1008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendorsprofile',
            name='profile_approved',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.profile_approved'),
        ),
    ]
