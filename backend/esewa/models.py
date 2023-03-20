from django.db import models

from stripe_card.models import Transaction,TransactionStatus
from app.models import App
from stripe_card.models import Environment
from esewa.api.serializers.credentialserializers import CredentialSerializer

# Create your models here.


class EsewaTransaction(models.Model,Transaction):
    app = models.ForeignKey(App, on_delete=models.RESTRICT,null=True)
    reference_id = models.CharField(max_length=255, unique=True) #esewa reference id when the success
    transaction_id = models.CharField(max_length=255, unique=True, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    transaction_status = models.CharField(
        max_length=255, choices=TransactionStatus.choices())
    status_code = models.CharField(max_length=10)
    remarks = models.CharField(max_length=255)
    message = models.CharField(max_length=255, null=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
    customer_email = models.CharField(max_length=255, null=True)
    request_ip = models.CharField(max_length=255, null=True)
    user_agent = models.CharField(max_length=255, null=True)
    is_test = models.BooleanField(
        default=False, verbose_name="Is test payment?")
    credential_type = models.CharField(
        max_length=255, null=True)
    customer_name = models.CharField(max_length=255, null=True)
    customer_phone = models.CharField(max_length=15, null=True)
    meta_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class EsewaCredential(models.Model):
    app = models.ForeignKey(App, on_delete=models.RESTRICT)
    base_url = models.CharField(max_length=255)
    secret_key = models.CharField(max_length=255)
    public_key = models.CharField(max_length=255)
    credential_type = models.CharField(
        max_length=255, verbose_name="Credential Used For", null=True)
    environment = models.CharField(
        max_length=255, verbose_name="Is test or live?", null=True, choices=Environment.choices())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def serialize(self):
        return CredentialSerializer(self).data