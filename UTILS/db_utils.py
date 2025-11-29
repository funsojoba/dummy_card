import uuid
from django.db import models
from django.http import Http404
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager



def generate_id():
    return uuid.uuid4().hex


class BaseAbstractModel(models.Model):
    id = models.CharField(
        primary_key=True, editable=False, default=generate_id, max_length=70
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
        ordering = ("-created_at",)

    def save(self, *args, **kwargs):
        super(BaseAbstractModel, self).save(*args, **kwargs)



class EnvManager(models.Manager):
    def for_request(self, request):
        return self.filter(
            organization=request.organization,
            environment=request.environment
        )
    
    def create_from_request(self, request, **kwargs):
        return self.create(
            organization=request.organization,
            environment=request.environment,
            **kwargs
        )
        

class BaseEnvModel(models.Model):
    organization = models.ForeignKey("AUTH_APP.Organization", on_delete=models.CASCADE)
    environment = models.CharField(max_length=20, choices=[("sandbox", "sandbox"), ("production", "production")])

    class Meta:
        abstract = True


def get_object_or_404(model, **kwargs):
    instance = model.objects.filter(**kwargs).first()
    if instance:
        return instance
    raise Http404



class OrganizationManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)