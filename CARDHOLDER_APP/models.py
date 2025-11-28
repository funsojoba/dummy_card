from django.db import models

# Create your models here.
from django.db import models
from UTILS.db_utils import BaseAbstractModel, BaseEnvModel, EnvManager
from AUTH_APP.models import Organization



class CardHolder(BaseAbstractModel, BaseEnvModel):
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

    objects = EnvManager()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"