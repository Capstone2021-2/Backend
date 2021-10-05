from .models import *
from rest_framework import serializers

class NutrientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutrient
        fields = ['name', 'upper', 'lower', 'unit']