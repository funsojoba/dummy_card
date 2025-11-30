import uuid
from CARD_APP.models import Card
from ORG_APP.service import OrganizationService
from UTILS.card_utils import generate_card_number, generate_cvv, generate_expiry
from UTILS.encrypt import derive_fernet_key, encrypt_string, decrypt_string
from UTILS.free_charges import FeeCharges
from CARDHOLDER_APP.service import CardholderService
from WEBHOOK_APP.service import WebhookService
from WEBHOOK_APP.models import CardEventType


from django.conf import settings

"""
Create card

fund_card
unload_card
card_debit_transaction
freeze_card
unfreeze_card
delete_card
"""


class CardService:
    
    @classmethod
    def create_card(cls, request, data):
        card_transaction_limit = data.get("card_transaction_limit")
        card_type = data.get("card_type")
        
        org_wallet_balance = OrganizationService.get_wallet_balance(
            organization=request.organization, 
            environment=request.environment
        )
        
        wallet_balance = org_wallet_balance.balance
        
        if wallet_balance < settings.TRANSACTION_THRESHOLD:
            return False, "Insufficient balance for transaction", 400
        
        try:
            card_number = generate_card_number(card_type=card_type)
            card_cvv = generate_cvv()
            card_expiry_date = generate_expiry()
            
            master_secret = settings.SECRET_KEY
            org_id = request.organization.id
            
            fernet_key = derive_fernet_key(org_id, master_secret)
            
            encrypted_card_number = encrypt_string(fernet_key, card_number)
            encrypted_card_cvv = encrypt_string(fernet_key, card_cvv)
            encrypted_card_expiry_date = encrypt_string(fernet_key, card_expiry_date)
            
            # get cardholder
            cardholder = CardholderService.get_cardholder(request=request, id=data.get("cardholder_id"))
            
            if not cardholder:
                return False, "Cardholder not found", 404
            
            if not cardholder.is_kyc_verified:
                return False, "Cardholder not verified", 400
            
            # creat card
            card = Card.objects.create_from_request(
                request=request,
                card_id = uuid.uuid1(),
                card_number = encrypted_card_number,
                card_name = f"{cardholder.first_name} {cardholder.last_name}",
                expiry_date = encrypted_card_expiry_date,
                cvv = encrypted_card_cvv,
                card_type=card_type,
                card_transaction_limit=card_transaction_limit,
                owner=cardholder
            )
            
            WebhookService.create_webhook_event(
                request=request, 
                event_type=CardEventType.CARD_CREATED_SUCCESS.value, 
                data={
                    "card_id": str(card.card_id),
                    "cardholder_id": str(card.owner.id)
                }
            )
            
            OrganizationService._debit_organization_wallet(
                request=request,
                amount=FeeCharges.CARD_ISSUING_FEE.value,
                description=f"Card issuing fee for {card.card_id}"
            )
            
            return True, card, 201
            
        except Exception as e:
            #TODO: log errors
            print("ERROR: ",e)
            return False, "Error creating card, please again", 500
        
    
    @classmethod
    def list_cards(cls, request, **kwargs):
        return Card.objects.for_request(request=request, is_active=True, is_deleted=False, **kwargs)
    
    @classmethod
    def get_card(cls, request, id):
        return Card.objects.for_request(request=request, id=id).first()
        
    @classmethod
    def decrypt_card_details(cls, request, id):
        
        card = cls.get_card(request=request, id=id)
        
        if card:
                
            master_secret = settings.SECRET_KEY
            org_id = request.organization.id
            
            fernet_key = derive_fernet_key(org_id, master_secret)
            
            decrypted_card_number = decrypt_string(fernet_key, card.card_number)
            decrypted_card_cvv = decrypt_string(fernet_key, card.cvv)
            decrypted_card_expiry_date = decrypt_string(fernet_key, card.expiry_date)
            
            return True, {
                "id": id,
                "card_number": decrypted_card_number,
                "cvv": decrypted_card_cvv,
                "expiry_date": decrypted_card_expiry_date
            }
        return False, "Card not found"
        
    
    
    @classmethod
    def get_card_details(cls, request, card_id):
        pass
    
    
    @classmethod
    def freeze_card(cls, request, card_id):
        pass
    
    @classmethod
    def unfreeze_card(cls, request, card_id):
        pass
    
    @classmethod
    def fund_card(cls, request, card_id, amount):
        pass
    
    @classmethod
    def unload_Card(cls, request, card_id, amount):
        pass
    
    @classmethod
    def get_card_balance(cls, request, card_id):
        pass
    
    @classmethod
    def get_card_transactions(cls, request, card_id):
        pass
    
    @classmethod
    def delete_card(cls, request, card_id):
        pass