from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class ProductDetailSerilizer(serializers.Serializer):
    """Product Detail Serializer For Payment Request

    Args:
        serializers (serializers): serializers
    """
    product_name = serializers.CharField(required=True, max_length=255)
    quantity = serializers.IntegerField(required=True)
    rate = serializers.IntegerField(required=True)
    total = serializers.IntegerField(required=True)


class WebPaymentSerializer(serializers.Serializer):
    """Prabhupay web payment serializer

    Args:
        Serializer (serializers): serializers
    """
    amount = serializers.IntegerField(required=True)
    reference_id = serializers.CharField(required=True, max_length=50)
    product_details = ProductDetailSerilizer(many=True)
    remarks = serializers.CharField(required=True, max_length=255)
    return_url = serializers.CharField(required=True, max_length=255)
    credential_type = serializers.CharField(required=True, max_length=255)
    environment = serializers.CharField(required=True, max_length=255)
