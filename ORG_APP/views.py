from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet

from rest_framework.decorators import action
from UTILS.response import Response

from ORG_APP.service import OrganizationService
from ORG_APP.serializers import EnvironmentSerializer
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
        