from rest_framework import serializers
from CARDHOLDER_APP.models import CardHolder



class CreateCardholderSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    country = serializers.CharField()
    state_region = serializers.CharField()
    
    
class CardholderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardHolder
        fields = "__all__"