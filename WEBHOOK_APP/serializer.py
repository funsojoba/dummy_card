from rest_framework import serializers
from WEBHOOK_APP.models import WebhookEndpoint, WebhookEvent, WebhookDelivery
from UTILS.enums import EnvironmentType

class CreateWebhookEndpointSerializer(serializers.Serializer):
    url = serializers.URLField()
    environment = serializers.ChoiceField(
        choices=[e.value for e in EnvironmentType]
    )
    secret = serializers.CharField()
    

class WebhookEndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebhookEndpoint
        fields = "__all__"
        
        
class WebhookDeliverySerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    
    def get_url(self, obj):
        endpoint = WebhookEndpointSerializer(obj.endpoint).data
        
        return endpoint.get("url")
    class Meta:
        model = WebhookDelivery
        fields = "__all__"
        

class WebhookEventSerializer(serializers.ModelSerializer):
    delivery = serializers.SerializerMethodField()
    
    def get_delivery(self, obj):
        deliveries = WebhookDelivery.objects.filter(event=obj)
        return WebhookDeliverySerializer(deliveries, many=True).data
    class Meta:
        model = WebhookEvent
        fields = "__all__"
        
