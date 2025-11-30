from django.db import models
from UTILS.db_utils import BaseAbstractModel, BaseEnvModel, EnvManager
from UTILS.enums import TransactionType, CardType, CardTransactionLimit


class Card(BaseAbstractModel, BaseEnvModel):
    card_id = models.CharField(max_length=50, unique=True)
    card_number = models.CharField(max_length=255, unique=True)
    card_name = models.CharField(max_length=255)
    expiry_date = models.CharField(max_length=255)
    cvv = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)
    card_type = models.CharField(max_length=20, default=CardType.MASTERCARD.value, choices=[(tag.value, tag.value) for tag in CardType])
    card_transaction_limit = models.IntegerField(choices=[(tag.value, tag.value) for tag in CardTransactionLimit], default=CardTransactionLimit.FIVE_THOUSAND.value)
    owner = models.ForeignKey('CARDHOLDER_APP.CardHolder', on_delete=models.CASCADE, related_name='cards')
    
    objects = EnvManager()
    
    def __str__(self):
        return f"{self.card_name} - {self.card_number}"



class Wallet(BaseAbstractModel, BaseEnvModel):
    balance = models.IntegerField()
    currency = models.CharField(max_length=10, default='USD')
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="card_wallet")
    owner = models.OneToOneField('CARDHOLDER_APP.CardHolder', on_delete=models.CASCADE, related_name='wallet')
    
    objects = EnvManager()
    
    def __str__(self):
        return f"Wallet of {self.owner.first_name} {self.owner.last_name} - Balance: {self.balance} {self.currency}"
    
    

class Transaction(BaseAbstractModel, BaseEnvModel):
    
    amount = models.IntegerField()
    transaction_type = models.CharField(max_length=20, choices=[(tag.value, tag.value) for tag in TransactionType])
    timestamp = models.DateTimeField(auto_now_add=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="transaction_card")
    description = models.TextField(blank=True, null=True)
    reference = models.CharField(max_length=256)
    old_balance = models.IntegerField()
    new_balance = models.IntegerField()
    meta_data = models.JSONField()
    
    objects = EnvManager()
    def __str__(self):
        return f"{self.transaction_type} of {self.amount} on {self.timestamp}"