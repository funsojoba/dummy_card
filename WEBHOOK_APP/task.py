import hmac
import json
import base64
import hashlib
import requests

from celery import shared_task
from celery.exceptions import RetryTaskException

from UTILS.generate_id import generate_hmac_signature
from WEBHOOK_APP.models import WebhookEvent, WebhookEndpoint, WebhookDelivery



@shared_task
def deliver_webhook(event_id):
    event = WebhookEvent.objects.get(event_id=event_id)
    endpoints = WebhookEndpoint.objects.filter(user=event.user, is_active=True)

    for endpoint in endpoints:
        signature = generate_hmac_signature(endpoint.secret, event.payload)

        headers = {
            "Content-Type": "application/json",
            "X-Webhook-Signature": signature,
            "X-Webhook-Event-ID": event.event_id,
            "X-Webhook-Event-Type": event.event_type,
        }

        response = requests.post(endpoint.url, json=event.payload, headers=headers)

        WebhookDelivery.objects.create(
            event=event,
            endpoint=endpoint,
            status_code=response.status_code,
            response_body=response.text,
            success=(200 <= response.status_code < 300),
        )

        if 200 <= response.status_code < 300:
            event.delivered = True
            event.save()
        else:
            raise RetryTaskException()  # Celery retry with exponential backoff