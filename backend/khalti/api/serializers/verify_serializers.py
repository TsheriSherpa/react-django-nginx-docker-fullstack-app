from rest_framework import serializers


class VerifySerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)
