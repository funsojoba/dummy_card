from uuid import uuid4
from django.utils import timezone
from WEBHOOK_APP.models import WebhookEvent
from WEBHOOK_APP.task import deliver_webhook



def create_webhook_event(user, event_type, data):
    event_id = uuid4().hex

    payload = {
        "id": event_id,
        "type": event_type,
        "version": "2025-01-01",
        "created_at": timezone.now().isoformat(),
        "data": data,
    }

    event = WebhookEvent.objects.create(
        event_id=event_id,
        event_type=event_type,
        payload=payload
    )

    deliver_webhook.delay(event.event_id)

    return event