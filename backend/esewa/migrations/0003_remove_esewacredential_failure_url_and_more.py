# Generated by Django 4.0.6 on 2022-08-15 04:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('esewa', '0002_esewatransaction_oid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='esewacredential',
            name='failure_url',
        ),
        migrations.RemoveField(
            model_name='esewacredential',
            name='success_url',
        ),
    ]
