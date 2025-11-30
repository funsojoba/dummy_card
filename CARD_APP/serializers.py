from rest_framework import serializers
from UTILS.enums import CardType, CardTransactionLimit

from CARD_APP.models import Card, Wallet, Transaction
from CARDHOLDER_APP.serializers import CardholderSerializer


class CreateCardSerializer(serializers.Serializer):
    card_type = serializers.ChoiceField(
        choices=[e.value for e in CardType]
    )
    card_transaction_limit = serializers.ChoiceField(
        choices=[e.value for e in CardTransactionLimit]
    )
    cardholder_id = serializers.CharField()
    
    
class DecrypteCardSerializer(serializers.Serializer):
    id = serializers.CharField()

class CardSerializer(serializers.ModelSerializer):
    owner = CardholderSerializer()
    class Meta:
        model = Card
        fields = "__all__"
        
        
        
class FundCardSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    reference = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    meta_data = serializers.JSONField(required=False)
    

class CardWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ("balance", "currency")
        

class CardTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ("id", "amount", "transaction_type", "timestamp", "description", "reference", "old_balance", "new_balance", "meta_data")