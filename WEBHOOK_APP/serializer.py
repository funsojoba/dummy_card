from rest_framework import serializers
from WEBHOOK_APP.models import WebhookEndpoint
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