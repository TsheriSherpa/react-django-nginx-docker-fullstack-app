from rest_framework import serializers


class AppAccessTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)
