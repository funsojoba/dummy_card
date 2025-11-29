import secrets
from django.db.models import Q
from AUTH_APP.models import Organization, APIToken
from UTILS.enums import EnvironmentType

from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken


"""
Signing up, you have access to the SandBox environment by default, 
access to production environment comes upon verification, is_verified=True, is_active=True
"""


class AuthService:
    @classmethod
    def sign_up_organization(cls, data: dict):
        
        password = data.get("password")
        hashed_password = make_password(password)
        email = data.get("email")
        
        if Organization.objects.filter(
            Q(phone_number=data.get("phone_number"))
            | Q(email=email)
            ).exists():
            return False, "Organization already exist"
        
        organization = Organization.objects.create(
            name=data.get("name"),
            country=data.get("country"),
            industry=data.get("industry"),
            email=email,
            phone_number=data.get("phone_number"),
            password=hashed_password,
            website=data.get("website")
        )
        
        
        return True, organization
    
    @classmethod
    def log_in_organizagion(cls, data: dict):
        email = data.get("email")
        password = data.get("password")
        
        organization = Organization.objects.filter(email=email)
        
        if not organization.exists():
            return False, "Invalid credentials"
        
        org = organization.first()
        
        org_password = org.password
        
        if not check_password(password=password, encoded=org_password):
            return False, "Invalid credentials"
        
        token = RefreshToken.for_user(org)
        data = {
            "token": {
                "refresh": str(token),
                "access": str(token.access_token),
            },
        }

        return True, data
    
    