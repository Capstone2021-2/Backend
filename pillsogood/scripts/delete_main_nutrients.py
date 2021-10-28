from api.models import MainNutrient

def run():
    queryset = MainNutrient.objects.all()
    queryset.delete()