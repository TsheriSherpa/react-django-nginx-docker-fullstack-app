from rest_framework import serializers


class EsewaVerifySerializer(serializers.Serializer):
    environment = serializers.CharField(required=True)
    credential_type = serializers.CharField(required=True)
    amount = serializers.CharField(required=True)
    reference_id = serializers.CharField(required=True)
    remarks = serializers.CharField(required=True)
    customer_name = serializers.CharField(required=False)
    customer_phone = serializers.CharField(required=False)
    customer_email = serializers.CharField(required=False)
