from api.models import AgeNutrient

def run():
    queryset = AgeNutrient.objects.all()
    queryset.delete()