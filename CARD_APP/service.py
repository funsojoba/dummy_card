import uuid
from django.conf import settings
from CARD_APP.models import Card, Wallet, Transaction
from ORG_APP.service import OrganizationService
from UTILS.card_utils import generate_card_number, generate_cvv, generate_expiry
from UTILS.encrypt import derive_fernet_key, encrypt_string, decrypt_string
from UTILS.free_charges import FeeCharges
from UTILS.enums import TransactionType, CardTransactionDescription
from CARDHOLDER_APP.service import CardholderService
from WEBHOOK_APP.service import WebhookService
from WEBHOOK_APP.models import CardEventType, TransactionEventType


from django.conf import settings
from django.utils import timezone

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
    def freeze_card(cls, request, card_id):
        try:
            card = cls.get_card(request=request, id=card_id)
            if card.is_active == False:
                return True, "Card is already frozen"

            card.is_active = False
            card.save()
            return True, "Card frozen successfully"
        except Exception as e:
            print("ERROR freezing card: ", e)
            return False, "Error freezing card"
    
    @classmethod
    def unfreeze_card(cls, request, card_id):
        try:
            card = cls.get_card(request=request, id=card_id)
            
            if card.is_active == True:
                return False, "Card is already unfrozen"
            
            card.is_active = True
            card.save()
            return True, card
        except Exception as e:
            print("ERROR unfreezing card: ", e)
            return False, "Error unfreezing card"
    
    
    @classmethod
    def get_card_wallet(cls, request, card):
        wallet = Wallet.objects.for_request(request=request, card=card)
        return wallet.first()
        
    @classmethod
    def _create_card_transaction(cls, request, card, amount, wallet, transaction_type, description, old_balance, new_balance, reference, meta_data=None):
        transaction = Transaction.objects.create_from_request(
            request=request, amount=amount, 
            transaction_type=transaction_type,
            wallet=wallet, card=card, description=description,
            old_balance=old_balance, new_balance=new_balance,
            reference = reference,
            meta_data = meta_data
            )
    
    @classmethod
    def _credit_card_wallet(cls, request, card, amount, reference=None, description="", meta_data={}):
        wallet = cls.get_card_wallet(request=request, card=card)
        
        if not reference:
            reference = "CDR:"+uuid.uuid1().hex
        
        if not description:
            description = CardTransactionDescription.CARD_CREDIT.value + f" of {str(amount)} with reference {reference}"
            
        old_balance = wallet.balance
        
        new_balance = old_balance + amount
        
        wallet.balance = new_balance
        wallet.save()
        
        cls._create_card_transaction(
            request=request, card=card, amount=amount,
            transaction_type=TransactionType.CREDIT.value,
            description=description, wallet=wallet,
            old_balance=old_balance, new_balance=new_balance,
            reference=reference, meta_data=meta_data
        )
        
        WebhookService.create_webhook_event(
            request=request,
            event_type=TransactionEventType.TRANSACTION_CREDIT_SUCCESS.value,
            data={
                "amount": amount,
                "reference": reference,
                "description": description,
                "meta_data": meta_data,
                "transaction_type": TransactionType.CREDIT.value,
                "currency": "USD" #Don't hard code
            }
        )
    
    @classmethod
    def _debit_card_wallet(cls, request, card, amount, reference=None, description="", meta_data={}):
        if not reference:
            reference = "DBR:"+uuid.uuid1().hex
            
        if not description:
            description = CardTransactionDescription.CARD_DEBIT.value + f" of {str(amount)} with reference {reference}"
            
        
        wallet = cls.get_card_wallet(request=request, card=card)
        old_balance = wallet.balance
        
        new_balance = old_balance - amount
        
        wallet.balance = new_balance
        wallet.save()
        
        cls._create_card_transaction(
            request=request, card=card, amount=amount,
            transaction_type=TransactionType.DEBIT.value,
            description=description, wallet=wallet,
            old_balance=old_balance, new_balance=new_balance,
            reference=reference, meta_data=meta_data
        )
        
        WebhookService.create_webhook_event(
            request=request,
            event_type=TransactionEventType.TRANSACTION_DEBIT_SUCCESS.value,
            data={
                "amount": amount,
                "reference": reference,
                "description": description,
                "meta_data": meta_data,
                "transaction_type": TransactionType.DEBIT.value,
                "currency": "USD" #Don't hard code
            }
        )
        
    
    @classmethod
    def fund_card(cls, request, card_id, amount, reference=None, description=None, meta_data={}):
        
        # TODO: handle idempotency, atomicity
        
        card = cls.get_card(request=request, id=card_id)
        card_org = card.organization
        
        org_wallet_balance = OrganizationService.get_wallet_balance(
            organization=card_org, environment=card.environment
        )
        
        if org_wallet_balance.balance < settings.TRANSACTION_THRESHOLD:
            return False, "Insufficient balance for transaction", 400
        
        if org_wallet_balance.balance < amount:
            return False, "Insufficient balance for transaction", 400
        
        try:
            OrganizationService._debit_organization_wallet(
                request=request, amount=amount, description=f"Card funding for {card_id}"
            )
            
            cls._credit_card_wallet(
                request=request, card=card, 
                amount=amount, reference=reference, 
                description=description,
                meta_data=meta_data
            )
            return True, "Card funded successfully", 201
        except Exception as e:
            print("ERROR *****",e)
            return False, "Error funding card", 400
         
        
    
    @classmethod
    def unload_Card(cls, request, card_id, amount, reference=None, description=None, meta_data={}):
        card = cls.get_card(request=request, id=card_id)
        card_org = card.organization
        
        org_wallet_balance = OrganizationService.get_wallet_balance(
            organization=card_org, environment=card.environment
        )
        
        card_wallet = cls.get_card_wallet(request=request, card=card)
        
        card_balance = card_wallet.balance
        
        if card_balance < amount:
            return False, "Insufficient card balance"
            
        cls._debit_card_wallet(
            request=request, card=card, 
            amount=amount, reference=reference, 
            description=description,
            meta_data=meta_data
        )
        
        
        OrganizationService._credit_organization_wallet(
                request=request, amount=amount, 
                description=f"Card unloading for {card_id}"
            )
        return True, "Card unload successful"
    
    @classmethod
    def get_card_balance(cls, request, card_id):
        card = cls.get_card(request=request, id=card_id)
        
        wallet = cls.get_card_wallet(request=request, card=card)
        
        return wallet
    
    @classmethod
    def get_card_transactions(cls, request, card_id):
        card = cls.get_card(request=request, id=card_id)
        transactions = Transaction.objects.for_request(
            request=request, card=card
        )
        return transactions
    
    @classmethod
    def delete_card(cls, request, card_id, deletion_reason=""):
        try:
            card = cls.get_card(request=request, id=card_id)
            
            card_balance = cls.get_card_wallet(request=request, card=card).balance
            
            if card_balance > 0:
                # unload card balance and credit to org wallet
                cls.unload_Card(
                    request=request, card_id=card_id, amount=card_balance,
                    description="Unloading card balance before deletion"
                )
                
                # credit org wallet
                OrganizationService._credit_organization_wallet(
                    request=request, amount=card_balance,
                    description=f"Card balance credit before deletion for card {card_id}"
                )
                
            
            if card.is_deleted:
                return "Card is already deleted"
            
            card.is_deleted = True
            card.deletion_reason = deletion_reason
            card.deleted_at = timezone.now()
            card.save()
            return None
        except Exception as e:
            print("ERROR deleting card: ", e)
            return "Error deleting card"