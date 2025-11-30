from rest_framework import status
from rest_framework.viewsets import ViewSet
from CARDHOLDER_APP.service import CardholderService
from CARDHOLDER_APP.serializers import CreateCardholderSerializer, CardholderSerializer

from UTILS.permissions import APITokenAuthentication, RequireAPIKey
from UTILS.response import Response, paginate_response



class CardholderViewSet(ViewSet):
    
    authentication_classes = [APITokenAuthentication]
    permission_classes = [RequireAPIKey]
    def create(self, request):
        
        serializer = CreateCardholderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        cardholder = CardholderService.create(request=request, data=serializer.validated_data)
        
        return Response(
            data = CardholderSerializer(cardholder).data,
            status = status.HTTP_201_CREATED
        )
        
    def list(self, request):
        cardholders = CardholderService.list_cardholder(request=request)
        
        return paginate_response(cardholders, CardholderSerializer, request=request)

    def retrieve(self, request, pk=None):
        cardholder = CardholderService.get_cardholder(request=request, id=pk)
        
        if not cardholder:
            return Response(
                errors = {
                    "message": "cardholder not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(
            data = CardholderSerializer(cardholder).data,
            status = status.HTTP_201_CREATED
        )