from django.db import models
from UTILS.db_utils import BaseAbstractModel
from AUTH_APP.models import Organization

# Create your models here.


class OrganizationWallet(BaseAbstractModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='org_wallet')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=10, default='USD')
    
    
class OrganzationTransaction(BaseAbstractModel):
    TRANSACTION_TYPES = [
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAWAL', 'Withdrawal'),
        ('TRANSFER', 'Transfer'),
        ('REFUND', 'Refund'),
    ]
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='org_transaction')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    balance_before = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    balance_after = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    