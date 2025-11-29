from rest_framework import serializers
from UTILS.enums import EnvironmentType
from ORG_APP.models import OrganizationWallet, OrganzationTransaction



class EnvironmentSerializer(serializers.Serializer):
    environment = serializers.ChoiceField(
        choices=[e.value for e in EnvironmentType]
    )
    

class OrganizationWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationWallet
        fields = "__all__"
        

class OrganizationTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganzationTransaction
        fields = "__all__"