# Generated by Django 4.0.6 on 2022-08-27 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imepay', '0003_imepaycredential_merchant_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='imepaytransaction',
            name='token',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]
