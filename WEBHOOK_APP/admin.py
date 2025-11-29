from django.contrib import admin

from WEBHOOK_APP.models import WebhookDelivery, WebhookEndpoint, WebhookEvent


admin.site.register((
    WebhookDelivery, WebhookEndpoint, WebhookEvent
))
