from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class PaymentVerifySerializer(serializers.Serializer):
    """Prabhupay web payment verify serializer

    Args:
        Serializer (serializers): serializers
    """
    reference_id = serializers.CharField(required=True, max_length=50)
    credential_type = serializers.CharField(required=True, max_length=255)
    environment = serializers.CharField(required=True, max_length=255)
