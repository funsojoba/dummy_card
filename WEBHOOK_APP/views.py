from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from WEBHOOK_APP.serializer import WebhookEventSerializer
from WEBHOOK_APP.service import WebhookService
from UTILS.response import paginate_response, Response




class WebhookViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        webhook_event = WebhookService.list_webhook(request=request)
        return paginate_response(webhook_event, WebhookEventSerializer, request=request)
    
    def retrieve(self, request, pk=None):
        webhook_event = WebhookService.get_webhook(request=request, event_id=pk)
        return Response(
            data=WebhookEventSerializer(webhook_event).data
        )
    
    @action(methods=['POST'], detail=False, url_path="resend-webhook/(?P<event_id>[^/.]+)")
    def resend_webhook(self, request, event_id=None):
        result = WebhookService.repush_webhook(
            request=request, event_id=event_id
        )
        
        if result:
            return Response(
                data={"message": "Webhhook repush initiated"},
                status=status.HTTP_202_ACCEPTED
            )
        
        return Response(
            errors={"message": "Webhook not found"},
            status=status.HTTP_404_NOT_FOUND
        )