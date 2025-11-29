import hmac
import json
import base64
import hashlib
import requests
from django.conf import settings

from celery import shared_task
# from celery.exceptions import RetryTaskException

from UTILS.encrypt import decrypt_string, derive_fernet_key
from UTILS.generate_id import generate_hmac_signature
from WEBHOOK_APP.models import WebhookEvent, WebhookEndpoint, WebhookDelivery



@shared_task
def deliver_webhook(event_id):
    event = WebhookEvent.objects.get(event_id=event_id)
    endpoints = WebhookEndpoint.objects.filter(organization=event.organization, is_active=True)

    for endpoint in endpoints:
        
        #Decrypt Secret
        master_secret = settings.SECRET_KEY
        org_id = endpoint.organization.id
        encrypted_secret = endpoint.secret
        fernet_key = derive_fernet_key(org_id, master_secret)
        
        secret = decrypt_string(fernet_key, encrypted_secret)
        
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
            organization=event.organization,
            environment=event.environment,
            status_code=response.status_code,
            response_body=response.text,
            success=(200 <= response.status_code < 300),
        )

        if 200 <= response.status_code < 300:
            event.delivered = True
            event.save()
        else:
            event.delivered = False
            event.save()
            # raise RetryTaskException()  # Celery retry with exponential backoff