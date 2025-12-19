import secrets
from datetime import datetime
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from AUTH_APP.models import Organization, APIToken
from WEBHOOK_APP.models import WebhookEndpoint, OrganizationWalletEventType
from WEBHOOK_APP.service import WebhookService
from ORG_APP.models import OrganizationWallet, OrganzationTransaction

from UTILS.encrypt import derive_fernet_key, encrypt_string
from UTILS.enums import TransactionType



from CARD_APP.models import Card, Transaction
from CARDHOLDER_APP.models import CardHolder



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
        org_trx = OrganzationTransaction.objects.filter(
            organization=organization,
            environment=environment
        )
        return org_trx.order_by("-created_at")
        
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
    def _credit_organization_wallet(cls, request, amount:int, description:str):
        
        organization = request.organization
        environment = request.environment
        
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
        # Send webhook
        WebhookService.create_webhook_event(
            request=request,
            event_type=OrganizationWalletEventType.WALLET_CREDITED.value,
            data={
                "amount": amount,
                "description": description,
                "balance_before": old_balance,
                "balance_after": new_balance,
            }
        )
        
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
    
    @classmethod
    def organization_statistics(cls, organization, month=None, year=None, environment="sandbox"):
        
        
        """_summary_

        Statistics such as total cards issued, total active cards, total wallet balance, total transactions etc
        Total Transaction volume over time
        Total Transaction volumne for the month, quarter, year
        Average transaction value
        
        Total active cards over time
        Total cards issued over time
        Total cards issued in a month, quarter, year
        
        
        Revenue generated over time
        Revenue generated in a month, quarter, year
        
        Expenses over time
        Expenses in a month, quarter, year
        """
        
        all_cards = Card.objects.filter(organization=organization, environment=environment)
        
        
        now = datetime.now()
        if not year: year = now.year
        
        if month and year:
            all_cards = all_cards.filter(
                created_at__month=month,
                created_at__year=year
            )
        elif year:
            all_cards = all_cards.filter(
                created_at__year=year
            )
        
        total_cards_issued = all_cards.count()
        total_active_cards = all_cards.filter(is_active=True).count()
        wallet = cls.get_wallet_balance(organization=organization, environment=environment)
        total_wallet_balance = wallet.balance if wallet else 0
        
        all_transactions = Transaction.objects.filter(organization=organization, environment=environment)
        
        if month and year:
            all_transactions = all_transactions.filter(
                created_at__month=month,
                created_at__year=year
            )
        elif year:
            all_transactions = all_transactions.filter(
                created_at__year=year
            )
        
        total_transaction_count = all_transactions.count()
        total_transaction_volume = all_transactions.aggregate(total_volume=models.Sum('amount'))['total_volume'] or 0
        average_transaction_value = all_transactions.aggregate(avg_value=models.Avg('amount'))['avg_value'] or 0
        
        statistics = {
            "total_cards_issued": total_cards_issued,
            "total_active_cards": total_active_cards,
            "total_wallet_balance": total_wallet_balance,
            "total_transaction_count": total_transaction_count,
            "total_transaction_volume": total_transaction_volume,
            "average_transaction_value": average_transaction_value,
        }
        return statistics
    
    @classmethod
    def generate_monthly_invoice(cls, organization, month, year, environment="sandbox"):
        # Placeholder for future implementation
        """_summary_
        
        Charge the organization a monthly invoice based on their usage
        100 cent per card issued
        50 cent per transaction
        100 cent maintenance fee per card

        Args:
            organization (_type_): _description_
            month (_type_): _description_
            year (_type_): _description_
            environment (str, optional): _description_. Defaults to "sandbox".
        """
        pass