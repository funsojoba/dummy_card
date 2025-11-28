from CARDHOLDER_APP.models import CardHolder



class CardholderService:
    @classmethod
    def create(cls, request, data):
        cardholder = CardHolder.objects.create_from_request(request=request,**data)
        return cardholder
    
    @classmethod
    def list_cardholder(cls, organization):
        return CardHolder.objects.filter(organization=organization)
    
    
    @classmethod
    def get_cardholder(cls, organization, id):
        return CardHolder.objects.filter(
                        id=id,
                        organization=organization).first()
        
    
    
    
    
    
    
        