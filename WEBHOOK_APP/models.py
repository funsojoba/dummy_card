from enum import Enum
from django.db import models
from UTILS.db_utils import BaseAbstractModel, BaseEnvModel, EnvManager



class WebhookEndpoint(BaseAbstractModel, BaseEnvModel):
    url = models.URLField()
    secret = models.CharField(max_length=255)  # For signing
    is_active = models.BooleanField(default=True)
    
    objects = EnvManager()
    
    def __str__(self):
        return self.organization.name + " - "+ self.url
    



class WebhookEvent(BaseAbstractModel, BaseEnvModel):
    event_id = models.CharField(max_length=64, unique=True)
    event_type = models.CharField(max_length=255)
    payload = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    delivered = models.BooleanField(default=False)
    attempts = models.IntegerField(default=1)
    
    objects = EnvManager()
    
    def __str__(self):
        return self.organization.name + " - "+ self.event_type
    
    
    
class WebhookDelivery(BaseAbstractModel, BaseEnvModel):
    event = models.ForeignKey(WebhookEvent, on_delete=models.CASCADE)
    endpoint = models.ForeignKey(WebhookEndpoint, on_delete=models.CASCADE)
    status_code = models.IntegerField(null=True)
    response_body = models.TextField(null=True)
    delivered_at = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)
    
    objects = EnvManager()
    
    def __str__(self):
        status = "SUCCESS" if self.success else "FAILURE"
        return self.organization.name + " - "+ self.event.event_type + " - " + status
    
    
    
    
    

class CardEventType(Enum):
    CARD_CREATED_SUCCESS = "card.created.success"
    CARD_UPDATED = "card.updated"
    CARD_DELETED = "card.deleted"
    CARD_BLOCKED = "card.blocked"
    CARD_UNBLOCKED = "card.unblocked"
    
class CardHolderEventType(Enum):
    CARDHOLDER_CREATED_SUCCESS = "cardholder.created.success"
    CARDHOLDER_CREATED_FAILURE = "cardholder.created.failure"
    CARDHOLDER_VERIFICATION_FAILURE = "cardholder.verification.failure"
    CARDHOLDER_VERIFICATION_SUCCESS = "cardholder.verification.success"

class WalletEventType(Enum):
    WALLET_FUNDED = "wallet.funded"
    WALLET_DEBITED = "wallet.debited"
    WALLET_CREATED = "wallet.created"
    WALLET_CLOSED = "wallet.closed"
    

class TransactionEventType(Enum):
    TRANSACTION_INITIATED = "transaction.debit"
    TRANSACTION_COMPLETED = "transaction.credit"
    TRANSACTION_FAILED = "transaction.reversed"
    TRANSACTION_REFUNDED = "transaction.refund"
    

class UserEventType(Enum):
    USER_REGISTERED = "user.registered"
    USER_UPDATED = "user.updated"
    USER_DEACTIVATED = "user.deactivated"
    USER_REACTIVATED = "user.reactivated"
    

