from uuid import uuid4
from django.utils import timezone
from WEBHOOK_APP.models import WebhookEvent, WebhookEndpoint
from WEBHOOK_APP.task import deliver_webhook



class WebhookService:
    
    def create_org_webhook(request, data):
        pass

    def create_webhook_event(request, event_type, data):
        event_id = uuid4().hex

        payload = {
            "id": event_id,
            "type": event_type,
            "version": "2025-01-01",
            "created_at": timezone.now().isoformat(),
            "data": data,
        }

        event = WebhookEvent.objects.create_from_request(
            request=request,
            event_id=event_id,
            event_type=event_type,
            payload=payload
        )

        deliver_webhook.delay(event.event_id)

        return event