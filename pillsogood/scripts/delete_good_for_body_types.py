from api.models import GoodForBodyType

def run():
    queryset = GoodForBodyType.objects.all()
    queryset.delete()