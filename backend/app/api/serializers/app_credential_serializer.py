from rest_framework import serializers

from prabhupay.api.serializers.credential_serializer import CredentialSerializer


class AppCredentialSerializer(serializers.Serializer):
    list = CredentialSerializer(many=True)
