from django.db import models
from UTILS.db_utils import BaseAbstractModel

"""
    first_name
    last_name
    email
    phone_number
    country
    state/region
    is_kyc_verified
    is_active
    is_flagged_for_fraud
    is_blacklisted
    
"""

class CardHolder(BaseAbstractModel):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    country = models.CharField(max_length=100)
    state_region = models.CharField(max_length=100)
    is_kyc_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_flagged_for_fraud = models.BooleanField(default=False)
    is_blacklisted = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"