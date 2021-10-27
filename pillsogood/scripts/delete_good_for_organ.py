from api.models import GoodForOrgan

def run():
    queryset = GoodForOrgan.objects.all()
    queryset.delete()