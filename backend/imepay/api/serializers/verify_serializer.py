
from rest_framework import serializers
class PaymentVerifySerializer(serializers.Serializer):

    reference_id = serializers.CharField(required=True, max_length=50)
    credential_type = serializers.CharField(required=True, max_length=255)
    environment = serializers.CharField(required=True, max_length=255)