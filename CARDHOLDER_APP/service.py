from CARDHOLDER_APP.models import CardHolder



class CardholderService:
    @classmethod
    def create(cls, request, data):
        cardholder = CardHolder.objects.create_from_request(request=request,**data)
        return cardholder
    
    @classmethod
    def list_cardholder(cls, request):
        return CardHolder.objects.for_request(request=request)
    
    
    @classmethod
    def get_cardholder(cls, request, id):
        cardholer_qs = CardHolder.objects.for_request(request=request)
        cardholder = cardholer_qs.filter(id=id).first()
        
        return cardholder or None
        
    
    
    
    
    
    
        