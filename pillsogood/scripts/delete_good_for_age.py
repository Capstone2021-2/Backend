from api.models import GoodForAge

def run():
    queryset = GoodForAge.objects.all()
    queryset.delete()