from rest_framework import serializers

from AUTH_APP.models import Organization



class SignUpSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    country = serializers.CharField()
    industry = serializers.CharField()
    phone_number = serializers.CharField()
    website = serializers.CharField()
    password = serializers.CharField(write_only=True)
    webhook_url= serializers.CharField(required=False)
    webhook_secret = serializers.CharField(required=False)
    
    
class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"
    
    
