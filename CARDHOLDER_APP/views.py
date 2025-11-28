from rest_framework import status
from rest_framework.viewsets import ViewSet
from CARDHOLDER_APP.service import CardholderService
from CARDHOLDER_APP.serializers import CreateCardholderSerializer, CardholderSerializer

from UTILS.permissions import APITokenAuthentication
from UTILS.response import Response



class CardholderViewSet(ViewSet):
    
    authentication_classes = [APITokenAuthentication]
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
        return Response(
            data = CardholderSerializer(cardholders, many=True).data,
            status = status.HTTP_201_CREATED
        )
    
    def retrieve(self, request, pk=None):
        cardholder = CardholderService.get_cardholder(request=request, id=pk)
        return Response(
            data = CardholderSerializer(cardholder).data,
            status = status.HTTP_201_CREATED
        )