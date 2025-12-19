from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

from CARD_APP.service import CardService
from CARD_APP.serializers import (
                CreateCardSerializer, CardSerializer, 
                DecrypteCardSerializer, FundCardSerializer, 
                CardWalletSerializer, CardTransactionSerializer)
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
        # TODO: filter by deleted, time range, active
        cards = CardService.list_cards(request=request)
        return paginate_response(
            cards, CardSerializer, request=request
        )
    
    def retrieve(self, request, pk=None):
        card = CardService.get_card(request=request, id=pk)
        return Response(
            data=CardSerializer(card).data
        )
        
    @action(methods=["POST"], detail=False, url_path="decrypt-card")
    def dercypt_card_details(self, request, id=None):
        serializer = DecrypteCardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        flag, response = CardService.decrypt_card_details(
            request=request,
            id=serializer.validated_data["id"]
        )
        if flag:
            return Response(data=response)
        return Response(
            errors={
                "message": response
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    
    @action(methods=['POST'], detail=False, url_path="(?P<id>[^/.]+)/fund-card")
    def fund_card(self, request, id):
        serializer = FundCardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        flag, response, status_code = CardService.fund_card(
            request=request, card_id=id, amount=serializer.validated_data["amount"],
            reference=serializer.validated_data.get("reference"),
            description=serializer.validated_data.get("description"),
            meta_data=serializer.validated_data.get("meta_data")
        )
        
        if flag:
            return Response(
                data = {
                    "message": response
                },
                status = status.HTTP_200_OK
            )
        else:
            return Response(
                errors = {
                    "message": response
                },
                status = status_code
            )
    
    @action(methods=['POST'], detail=False, url_path="(?P<id>[^/.]+)/unload-card")
    def unload_card(self, request, id):
        serializer = FundCardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        flag, response = CardService.unload_Card(
            request=request, card_id=id, amount=serializer.validated_data["amount"],
            reference=serializer.validated_data.get("reference"),
            description=serializer.validated_data.get("description"),
            meta_data=serializer.validated_data.get("meta_data")
        )
        
        if flag:
            return Response(
                data = {
                    "message": response
                },
                status = status.HTTP_200_OK
            )
        else:
            return Response(
                errors = {
                    "message": response
                },
                status = status.HTTP_400_BAD_REQUEST
            )
    
    
    
    @action(methods=['GET'], detail=False, url_path="(?P<id>[^/.]+)/balance")
    def get_card_balance(self, request, id):
        wallet = CardService.get_card_balance(
            request=request, card_id=id
        )
        return Response(
            data=CardWalletSerializer(wallet).data
        )
    
    @action(methods=['GET'], detail=False, url_path="(?P<id>[^/.]+)/transactions")
    def get_card_transaction(self, request, id):
        transaction = CardService.get_card_transactions(
            request=request, card_id=id
        )
        return paginate_response(
            transaction, CardTransactionSerializer, request=request
        )
    
    @action(methods=['POST'], detail=False, url_path="(?P<id>[^/.]+)/freeze")
    def freeze_card(self, request, id):
        flag, response = CardService.freeze_card(
            request=request, card_id=id
        )
        if flag:
            return Response(
                data={
                    "message": response
                },
                status=status.HTTP_200_OK
            )
        return Response(
            errors={
                "message": response
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(methods=['POST'], detail=False, url_path="(?P<id>[^/.]+)/unfreeze")
    def unfreeze_card(self, request, id):
        flag, response = CardService.unfreeze_card(
            request=request, card_id=id
        )
        if flag:
            return Response(
                data=CardSerializer(response).data,
                status=status.HTTP_200_OK
            )
        return Response(
            errors={
                "message": response
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    
    def destroy(self, request, pk=None):
        response = CardService.delete_card(
            request=request, card_id=pk
        )
        if response is None:
            return Response(
                data={
                    "message": "Card deleted successfully"
                },
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            errors={
                "message": response
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    