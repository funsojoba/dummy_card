from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.decorators import action
from UTILS.response import Response

from AUTH_APP.serializers import SignUpSerializer, OrganizationSerializer
from AUTH_APP.service import AuthService




class AuthViewSet(ViewSet):
    
    @action(methods=["POST"], detail=False, url_path="sign-up")
    def signup(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        flag, signup = AuthService.sign_up_organization(data=serializer.validated_data)
        
        if not flag:
            return Response(
                errors={"message": signup},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            data=OrganizationSerializer(signup).data,
            status=status.HTTP_201_CREATED
        )