# from django.shortcuts import render
from .models import *
from rest_framework import viewsets
from .serializer import *
from rest_framework import permissions

class NutrientViewSet(viewsets.ModelViewSet):
    queryset = Nutrient.objects.all()
    serializer_class = NutrientSerializer
    # permission_classes = [permissions.IsAuthenticated]