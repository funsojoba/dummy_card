import secrets
from django.utils import timezone
from django.db.models import Q
from AUTH_APP.models import Organization, APIToken, WebhookSettings
from UTILS.enums import EnvironmentType

from django.contrib.auth.hashers import make_password, check_password



"""
Signing up, you have access to the SandBox environment by default, 
access to production environment comes upon verification, is_verified=True, is_active=True
"""


class AuthService:
    @classmethod
    def sign_up_organization(cls, data: dict):
        
        webhook_url = data.get("webhook_url")
        webhook_secret = data.get("webhook_secret")
        
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
        
        if webhook_url and webhook_secret:
            WebhookSettings.objects.create(
                webhook_url=webhook_url,
                secret=webhook_secret,
                environment=EnvironmentType.SANDBOX.value
            )
        
        return True, organization
    
    @classmethod
    def log_in_organizagion(cls, data: dict):
        email = data.get("email")
        password = data.get("password")
        
        organization = Organization.objects.filter(email=email)
        
        if not organization.exists():
            return False, "Invalid credentials"
        
        org_password = organization.first().password
        
        if not check_password(password=password, encoded=org_password):
            return False, "Invalid credentials"
        
        token_data = {
            "access": "random shit",
            "refresh": "another random shit"
        }
        return True, token_data
    
    
    @classmethod
    def generate_api_key(cls, organization, environment):
        secret = secrets.token_hex(32)
        key_id = secrets.token_hex(4)
        
        environment_prefix_mapper = {
            "sandbox": "sk_sandbox",
            "production": "sk_production"
        }
        
        api_key = f"{environment_prefix_mapper[environment]}:{key_id}:{secret}"
    
        key_value = f"{api_key}:{organization.id}"
        
        hashed_api_key = make_password(key_value)
        
        APIToken.objects.create(
            organization=organization,
            token=hashed_api_key,
            environment=environment,
            key_id=key_id,
            expires_at=timezone.now() + timezone.timedelta(days=182)
        )
        
        return api_key
    
    