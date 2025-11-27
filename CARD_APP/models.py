from django.db import models
from UTILS.db_utils import BaseAbstractModel




"""
card_id
card_number
card_name
expiry_date
cvv
is_active
is_blocked
owner (ForeignKey to CardHolder)
card_number

"""

class Card(BaseAbstractModel):
    card_id = models.CharField(max_length=50, unique=True)
    card_number = models.CharField(max_length=16, unique=True)
    card_name = models.CharField(max_length=100)
    expiry_date = models.DateField()
    cvv = models.CharField(max_length=4)
    is_active = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)
    owner = models.ForeignKey('CARD_APP.CardHolder', on_delete=models.CASCADE, related_name='cards')
    
    def __str__(self):
        return f"{self.card_name} - {self.card_number}"



class Wallet(BaseAbstractModel):
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=10, default='USD')
    owner = models.OneToOneField('CARD_APP.CardHolder', on_delete=models.CASCADE, related_name='wallet')
    
    def __str__(self):
        return f"Wallet of {self.owner.first_name} {self.owner.last_name} - Balance: {self.balance} {self.currency}"
    
    

class Transaction(BaseAbstractModel):
    TRANSACTION_TYPES = [
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAWAL', 'Withdrawal'),
        ('TRANSFER', 'Transfer'),
        ('REFUND', 'Refund'),
    ]
    
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    wallet = models.ForeignKey('CARD_APP.Wallet', on_delete=models.CASCADE, related_name='transactions')
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.transaction_type} of {self.amount} on {self.timestamp}"