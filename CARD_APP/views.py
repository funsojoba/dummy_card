from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

from CARD_APP.service import CardService
from CARD_APP.serializers import CreateCardSerializer, CardSerializer, DecrypteCardSerializer, FundCardSerializer
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
    