from enum import Enum
from django.db import models
from app.models import App
from stripe_card.api.serializers.credential_serializer import CredentialSerializer


class TransactionStatus(Enum):
    INITIATED = "INITIATED"
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

    @classmethod
    def choices(cls) -> tuple:
        return tuple((i.name, i.value) for i in cls)


class Environment(Enum):
    TEST = "TEST"
    LIVE = "LIVE"

    @classmethod
    def choices(cls) -> tuple:
        return tuple((i.name, i.value) for i in cls)


class Transaction():
    def isSuccess(self) -> bool:
        return True if self.transaction_status == TransactionStatus.COMPLETED.value else False


class StripeTransaction(models.Model, Transaction):
    app = models.ForeignKey(App, on_delete=models.RESTRICT)
    reference_id = models.CharField(max_length=255, unique=True)
    transaction_id = models.CharField(max_length=255, unique=True, null=True)
    payment_intent = models.JSONField(null=True)
    charge_object = models.JSONField(null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    currency = models.CharField(max_length=255, null=-True)
    transaction_status = models.CharField(
        max_length=255, choices=TransactionStatus.choices())
    remarks = models.CharField(max_length=255)
    message = models.CharField(max_length=255, null=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
    customer = models.CharField(max_length=255, null=True)
    customer_email = models.CharField(max_length=255, null=True)
    customer_name = models.CharField(max_length=255, null=True)
    customer_phone = models.CharField(max_length=255, null=True)
    request_ip = models.CharField(max_length=255, null=True)
    user_agent = models.CharField(max_length=255, null=True)
    credential_type = models.CharField(
        max_length=255, null=True)
    is_test = models.BooleanField(
        default=False, verbose_name="Is test payment?")
    meta_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class StripeCredential(models.Model):
    app = models.ForeignKey(App, on_delete=models.RESTRICT)
    base_url = models.CharField(max_length=255)
    secret_key = models.CharField(max_length=255)
    publishable_key = models.CharField(max_length=255)
    credential_type = models.CharField(
        max_length=255, verbose_name="Credential Used For", null=True)
    environment = models.CharField(
        max_length=255, null=True, choices=Environment.choices())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def serialize(self):
        return CredentialSerializer(self).data
