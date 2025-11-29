import uuid

from django.db import models
from UTILS.db_utils import BaseAbstractModel, OrganizationManager
from UTILS.enums import EnvironmentType

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


def generate_id():
    return uuid.uuid4().hex



class Organization(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(
        primary_key=True, editable=False, default=generate_id, max_length=70
    )
    name = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    website = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)  # Hashed password
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = OrganizationManager()
    
    def __str__(self):
        return f"{self.name}"
    
    
    
class Member(BaseAbstractModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='members')
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=100)  # e.g., Admin, User, Manager
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email} ({self.organization.name})"
    

class APIToken(BaseAbstractModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='api_tokens')
    token = models.CharField(max_length=255, unique=True)
    environment = models.CharField(max_length=50, choices=[(tag.value, tag.value) for tag in EnvironmentType])
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    key_id = models.CharField(max_length=32, unique=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Token for {self.organization.name} - Active: {self.is_active}"
    
