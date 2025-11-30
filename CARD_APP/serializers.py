from rest_framework import serializers
from UTILS.enums import CardType, CardTransactionLimit

from CARD_APP.models import Card
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
        