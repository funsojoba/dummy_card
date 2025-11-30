from rest_framework import status
from rest_framework.viewsets import ViewSet

from CARD_APP.service import CardService
from CARD_APP.serializers import CreateCardSerializer, CardSerializer
from UTILS.permissions import APITokenAuthentication, RequireAPIKey
from UTILS.response import Response, paginate_response


class CardViewSet(ViewSet):
    authentication_classes = [APITokenAuthentication]
    permission_classes = [RequireAPIKey]
    def create(self, request):

        serializer = CreateCardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        flag, response, status_code = CardService.create_card(request=request, data=serializer.validated_data)
        
        if not flag:
            return Response(
                errors={
                    "message": response
                },
                status=status_code
            )
        return Response(
            data=CardSerializer(response).data,
            status=status_code
        )
        
    def list(self, request):
        cards = CardService.list_cards(request=request)
        return paginate_response(
            cards, CardSerializer, request=request
        )