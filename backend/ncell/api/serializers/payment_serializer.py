from rest_framework import serializers


class PaymentSerializer(serializers.Serializer):
    is_mobile = serializers.BooleanField(required=True)
    amount = serializers.IntegerField(required=True)
    reference_id = serializers.CharField(required=True, max_length=50)
    remarks = serializers.CharField(required=False, max_length=255)
    return_url = serializers.CharField(required=True, max_length=255)
    credential_type = serializers.CharField(required=True, max_length=255)
    environment = serializers.CharField(required=True, max_length=255)
