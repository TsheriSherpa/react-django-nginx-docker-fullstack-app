from rest_framework import serializers


class CredentialSerializer(serializers.Serializer):
    type = serializers.CharField(required=False)
    merchant_id = serializers.CharField(max_length=255)
    merchant_password = serializers.CharField(max_length=255)
    credential_type = serializers.CharField(max_length=255)
    environment = serializers.CharField(max_length=255)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['type'] = 'prabhupay'
        return data
