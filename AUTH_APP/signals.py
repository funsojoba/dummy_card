from django.db.models.signals import post_save
from django.dispatch import receiver

from AUTH_APP.models import Organization
from ORG_APP.models import OrganizationWallet



@receiver(post_save, sender=Organization)
def create_org_wallet(sender, instance, created, **kwargs):
    if not created:
        return

    # Create wallet only on first creation
    OrganizationWallet.objects.create(organization=instance)