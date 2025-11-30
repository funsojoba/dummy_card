from django.db.models.signals import post_save
from django.dispatch import receiver


from CARD_APP.models import Wallet, Card



@receiver(post_save, sender=Card)
def create_card_wallet(sender, instance, created, **kwargs):
    if not created:
        return
    
    Wallet.objects.create(
            card=instance, 
            environment=instance.environment, 
            organization=instance.organization, 
            )