# Generated by Django 4.0.6 on 2022-08-29 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imepay', '0003_imepaycredential_merchant_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imepaytransaction',
            name='transaction_status',
            field=models.CharField(choices=[('INITIATED', 'INITIATED'), ('PENDING', 'PENDING'), ('COMPLETED', 'COMPLETED'), ('FAILED', 'FAILED'), ('CANCELLED', 'CANCELLED')], max_length=255),
        ),
    ]
