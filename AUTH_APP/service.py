import secrets
from django.utils import timezone
from AUTH_APP.models import Organization, APIToken, WebhookSettings
from UTILS.enums import EnvironmentType

from django.contrib.auth.hashers import make_password, check_password



"""
Signing up, you have access to the SandBox environment by default, 
access to production environment comes upon verification, is_verified=True, is_active=True
"""


class AuthService:
    @classmethod
    def sign_up_organization(cls, data:dict):
        
        webhook_url = data.get("webhook_url")
        secret = data.get("webhook_secret")
        
        password = data.get("password")
        hashed_password = make_password(password)
        
        organization = Organization.objects.create(
            name=data.get("name"),
            country=data.get("country"),
            industry=data.get("industry"),
            email=data.get("email"),
            phone_number=data.get("phone_number"),
            password=hashed_password,
            website=data.get("website")
        )
        
        if webhook_url and secret:
            WebhookSettings.objects.create(
                webhook_url=webhook_url,
                secret=secret,
                environment=EnvironmentType.SANDBOX.value
            )
        
        return organization
    
    
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
    
    @classmethod
    def verify_api_key(cls, raw_key):
        import pdb ; pdb.set_trace()
        """
        Verify raw key; return APIToken instance on success, else None.
        raw_key expected as: prefix_keyid_secret
        """
        try:
            # split into three parts only (prefix, key_id, secret)
            prefix, key_id, secret = raw_key.split(":", 2)
        except Exception:
            return None

        try:
            token_obj = APIToken.objects.filter(key_id=key_id, is_active=True).first()
            if not token_obj:
                return None
            
            
            computed_secret = f"{raw_key}:{token_obj.organization.id}"
            
            if not check_password(computed_secret, token_obj.token):
                return None

            if token_obj.expires_at < timezone.now():
                return None
            return token_obj
        
        except APIToken.DoesNotExist:
            return None