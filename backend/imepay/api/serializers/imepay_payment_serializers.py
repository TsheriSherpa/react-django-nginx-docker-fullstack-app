"""Imepay Web Callback Serializer
"""
import base64
from datetime import datetime
from rest_framework import serializers
from imepay.api.services.imepay_service import ImePayService
from imepay.models import ImePayTransaction

class WebPaymentSerializer(serializers.Serializer):
    """Imepay Web Topup Callback Serializer

    Extends:
        serializers.Serializer

    Variables:
        data {str}
    """
    amount = serializers.IntegerField(required=True)
    reference_id = serializers.CharField(required=True, max_length=50)
    remarks = serializers.CharField(required=True, max_length=255)
    success_url = serializers.CharField(required=True, max_length=255)
    credential_type = serializers.CharField(required=True, max_length=255)
    environment = serializers.CharField(required=True, max_length=255)
