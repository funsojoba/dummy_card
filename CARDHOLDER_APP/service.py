from CARDHOLDER_APP.models import CardHolder

from WEBHOOK_APP.service import WebhookService
from WEBHOOK_APP.models import CardHolderEventType


class CardholderService:
    @classmethod
    def create(cls, request, data):
        cardholder = CardHolder.objects.create_from_request(request=request,**data)
        
        WebhookService.create_webhook_event(
            request=request,
            event_type=CardHolderEventType.CARDHOLDER_CREATED_SUCCESS.value,
            data={
                "message": "testing"
            }
        )
        return cardholder
    
    @classmethod
    def list_cardholder(cls, request):
        return CardHolder.objects.for_request(request=request)
    
    
    @classmethod
    def get_cardholder(cls, request, id):
        cardholer_qs = CardHolder.objects.for_request(request=request)
        cardholder = cardholer_qs.filter(id=id).first()
        
        return cardholder or None
        
    
    
    
    
    
    
        