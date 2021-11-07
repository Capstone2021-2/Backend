from api.models import Brand
from api.models import GoodForLifeStyle

def run():
    queryset = GoodForLifeStyle.objects.all()
    queryset.delete()