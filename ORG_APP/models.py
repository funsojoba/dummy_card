from django.db import models
from UTILS.db_utils import BaseAbstractModel
from AUTH_APP.models import Organization

from UTILS.enums import TransactionType, EnvironmentType


class OrganizationWallet(BaseAbstractModel):
    organization = models.OneToOneField(Organization, on_delete=models.CASCADE, related_name='org_wallet')
    balance = models.IntegerField()
    currency = models.CharField(max_length=10, default='USD')
    environment = models.CharField(max_length=50, choices=[(tag.value, tag.value) for tag in EnvironmentType])
    
    
class OrganzationTransaction(BaseAbstractModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='org_transaction')
    amount = models.IntegerField()
    transaction_type = models.CharField(max_length=20, choices=[(tag.value, tag.value) for tag in TransactionType])
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    balance_before = models.IntegerField()
    balance_after = models.IntegerField()
    environment = models.CharField(max_length=50, choices=[(tag.value, tag.value) for tag in EnvironmentType])
    
    