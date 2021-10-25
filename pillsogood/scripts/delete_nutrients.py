from api.models import Nutrient

def run():
    queryset = Nutrient.objects.all()
    queryset.delete()