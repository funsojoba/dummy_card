
from django.db import models
from UTILS.db_utils import BaseAbstractModel

from UTILS.enums import EnvironmentType





class Organization(BaseAbstractModel):
    name = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    website = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)  # Hashed password
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
    
    
    
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
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Token for {self.organization.name} - Active: {self.is_active}"
    

class WebhookSettings(BaseAbstractModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='webhook_secrets')
    webhook_url = models.URLField()
    environment = models.CharField(max_length=50, choices=[(tag.value, tag.value) for tag in EnvironmentType])
    secret = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Webhook Secret for {self.organization.name} - Active: {self.is_active}"