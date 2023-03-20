from rest_framework import serializers

class CredentialSerializer(serializers.Serializer):
    base_url=serializers.CharField(max_length=255)
    module=serializers.CharField(max_length=255)
    api_username=serializers.CharField(max_length=255)
    password=serializers.CharField(max_length=255)
    merchant_code=serializers.CharField(max_length=255)

    def to_representation(self,instance):
        data=super.to_representation(instance)
        data['type']='imepay'
        return data

