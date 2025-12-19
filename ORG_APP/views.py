from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet

from rest_framework.decorators import action
from UTILS.response import Response, paginate_response

from ORG_APP.service import OrganizationService
from ORG_APP.serializers import EnvironmentSerializer, OrganizationTransactionSerializer, OrganizationWalletSerializer
from WEBHOOK_APP.serializer import CreateWebhookEndpointSerializer, WebhookEndpointSerializer
from AUTH_APP.serializers import OrganizationSerializer



class OrganizationViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    
    @action(methods=["GET"], detail=False, url_path="profile")
    def get_profile(self, request):
        return Response(
            data=OrganizationSerializer(request.user).data
        )
    
    def invite_member(self, request):
        pass
    
    @action(methods=["POST"], detail=False, url_path="generate-api_key")
    def generate_api_key(self, request):
        serializer = EnvironmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        api_key = OrganizationService.generate_api_key(
            organization=request.user,
            environment=serializer.validated_data["environment"]
        )
        return Response(
            data={'api_key': api_key}
        )
        
    # setup webhook
    @action(methods=["POST"], detail=False, url_path="webhook-endpoint")
    def setup_webhook(self,request):
        serializer = CreateWebhookEndpointSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        webhook = OrganizationService.setup_webhook(
            organization=request.user,
            data=serializer.validated_data
        )
        
        return Response(
            data=WebhookEndpointSerializer(webhook).data
        )
    
    @action(methods=["GET"], detail=False, url_path="wallet-balance")
    def get_wallet_balance(self, request):
        environment = request.GET.get("environment", "sandbox")
        wallet_balance = OrganizationService.get_wallet_balance(organization=request.user, environment=environment)
        return Response(
            data=OrganizationWalletSerializer(wallet_balance).data
        )
    
    @action(methods=["GET"], detail=False, url_path="wallet-transactions")
    def get_wallet_transactions(self, request):
        environment = request.GET.get("environment", "sandbox")
        wallet_balance = OrganizationService.get_wallet_transaction(organization=request.user, environment=environment)
        return paginate_response(
            wallet_balance, OrganizationTransactionSerializer, request=request
        )
        
        
    @action(methods=["GET"], detail=False, url_path="statistics")
    def organization_statistics(self, request):
        environment = request.GET.get("environment", "sandbox")
        month = request.GET.get("month")
        year = request.GET.get("year")
        stats = OrganizationService.organization_statistics(
            organization=request.user,
            environment=environment,
            month=month,
            year=year
        )
        return Response(
            data=stats
        )
        
        