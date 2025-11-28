from rest_framework import status
from rest_framework.viewsets import ViewSet
from CARDHOLDER_APP.service import CardholderService
from CARDHOLDER_APP.serializers import CreateCardholderSerializer, CardholderSerializer

from UTILS.permissions import APITokenAuthentication
from UTILS.response import Response



class CardholderViewSet(ViewSet):
    
    authentication_classes = [APITokenAuthentication]
    def create(self, request):
        
        org = request.organization
        environment = request.environment
        
        print("ORGANIZATION", environment)
        
        serializer = CreateCardholderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        cardholder = CardholderService.create(request=request, data=serializer.validated_data)
        
        return Response(
            data = CardholderSerializer(cardholder).data,
            status = status.HTTP_201_CREATED
        )