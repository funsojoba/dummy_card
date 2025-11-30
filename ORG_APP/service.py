import secrets
from django.conf import settings
from django.utils import timezone
from AUTH_APP.models import Organization, APIToken
from WEBHOOK_APP.models import WebhookEndpoint, OrganizationWalletEventType
from WEBHOOK_APP.service import WebhookService
from ORG_APP.models import OrganizationWallet, OrganzationTransaction

from UTILS.encrypt import derive_fernet_key, encrypt_string
from UTILS.enums import TransactionType

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
        
    @classmethod
    def get_wallet_balance(cls, organization, environment):
        return OrganizationWallet.objects.filter(organization=organization, environment=environment).first()
    
    @classmethod
    def get_wallet_transaction(cls, organization, environment):
        return OrganzationTransaction.objects.filter(
            organization=organization,
            environment=environment
        )
        
    @classmethod
    def _create_wallet_transaction(cls, organization, environment, amount, transaction_type, description, balance_before, balance_after):
        return OrganzationTransaction.objects.create(
            amount=amount,
            organization=organization,
            environment=environment,
            transaction_type=transaction_type,
            description=description,
            balance_after=balance_after,
            balance_before=balance_before
        )
    
        
    @classmethod
    def _credit_organization_wallet(cls, organization, environment, amount:int, description:str):
        old_balance_query = cls.get_wallet_balance(organization=organization, environment=environment)
        old_balance = 0
        
        if old_balance_query:
            old_balance = old_balance_query.balance
            
        new_balance = old_balance + amount
        
        old_balance_query.balance = new_balance
        old_balance_query.save()
        
        cls._create_wallet_transaction(
            organization=organization,
            environment=environment,
            transaction_type=TransactionType.CREDIT.value,
            amount=amount,
            description=description, 
            balance_after=new_balance, balance_before=old_balance
        )
        #TODO: Send webhook
        
        
        return True
    
    @classmethod
    def _debit_organization_wallet(cls, request, amount:int, description:str):
        
        organization = request.organization
        environment = request.environment
        
        old_balance_query = cls.get_wallet_balance(organization=organization, environment=environment)
        old_balance = 0
        
        if old_balance_query:
            old_balance = old_balance_query.balance
            
        new_balance = old_balance - amount
        
        old_balance_query.balance = new_balance
        old_balance_query.save()
        
        cls._create_wallet_transaction(
            organization=organization,
            environment=environment,
            transaction_type=TransactionType.DEBIT.value,
            amount=amount,
            description=description, 
            balance_after=new_balance, balance_before=old_balance
        )
        # Send webhook
        WebhookService.create_webhook_event(
            request=request,
            event_type=OrganizationWalletEventType.WALLET_DEBITED.value,
            data={
                "amount": amount,
                "description": description,
                "balance_before": old_balance,
                "balance_after": new_balance,
            }
        )
        
        return True