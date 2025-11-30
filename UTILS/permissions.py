from rest_framework import authentication, exceptions
from UTILS.generate_id import verify_api_key
from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission

class APITokenAuthentication(authentication.BaseAuthentication):
    """
    Authenticates requests with X-API-KEY header.
    Returns (organization, None) as the `user` so views can access request.user or request.organization.
    """

    def authenticate(self, request):
        raw_key = request.headers.get("X-API-KEY") or request.META.get("HTTP_X_API_KEY")
        
        if not raw_key:
            return None
        
        # if not raw_key:
        #     raise AuthenticationFailed("Missing X-API-KEY header")

        token_obj = verify_api_key(raw_key)
        if not token_obj:
            raise AuthenticationFailed("Invalid or expired API key")

        # We want a "user" object. DRF expects (user, auth). We'll attach organization onto request.
        # Option A: return (token_obj.organization, None) but must be a User-compatible object for permissions.
        # Simpler: attach organization to request and return (AnonymousUser, token_obj).
        
        request.organization = token_obj.organization
        request.api_token = token_obj
        request.environment = token_obj.environment
        return (AnonymousUser(), token_obj)  
    
    


class RequireAPIKey(BasePermission):
    """
    Only allow access if the request was authenticated via API key.
    """

    def has_permission(self, request, view):
        return hasattr(request, "api_token")