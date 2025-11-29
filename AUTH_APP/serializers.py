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

    
class LogInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    
