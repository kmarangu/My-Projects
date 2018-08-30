# Generated by Django 2.0.2 on 2018-07-31 07:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20180731_0935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile_approved',
            name='approved',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='vendorsprofile',
            name='profile_approved',
            field=models.ForeignKey(default='No', on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.profile_approved'),
        ),
    ]