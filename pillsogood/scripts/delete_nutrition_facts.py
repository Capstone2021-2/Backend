from api.models import NutritionFact

def run():
    queryset = NutritionFact.objects.all()
    queryset.delete()