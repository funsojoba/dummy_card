from rest_framework import serializers
from UTILS.enums import EnvironmentType



class EnvironmentSerializer(serializers.Serializer):
    environment = serializers.ChoiceField(
        choices=[e.value for e in EnvironmentType]
    )