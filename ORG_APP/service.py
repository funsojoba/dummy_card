import secrets
from django.conf import settings
from django.utils import timezone
from AUTH_APP.models import Organization, APIToken
from WEBHOOK_APP.models import WebhookEndpoint

from UTILS.encrypt import derive_fernet_key, encrypt_string

from django.contrib.auth.hashers import make_password, check_password


# Set up webhook, URL and Key
# generate API key
# Request logs
# webhook logs
class OrganizationService:
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
        
        existing_api_key = APIToken.objects.filter(
            organization=organization,
            environment=environment,
            is_active=True
        )
        
        if existing_api_key:
            existing_api_key.delete()
        
        APIToken.objects.create(
            organization=organization,
            token=hashed_api_key,
            environment=environment,
            key_id=key_id,
            expires_at=timezone.now() + timezone.timedelta(days=182)
        )
        
        return api_key
    
    @classmethod
    def get_profile(cls, organization):
        return Organization.objects.filter(id=organization.id).first()
    
    @classmethod
    def setup_webhook(cls, organization, data):
        master_secret = settings.SECRET_KEY
        org_id = organization.id
        
        fernet_key = derive_fernet_key(org_id, master_secret)
        
        encrypted_secret = encrypt_string(fernet_key, data.get("secret"))
        
        webhook = WebhookEndpoint.objects.create(
            environment=data.get("environment"),
            organization=organization,
            url=data.get("url"),
            secret=encrypted_secret
        )
        return webhook
        
        