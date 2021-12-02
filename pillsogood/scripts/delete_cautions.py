from api.models import Caution

def run():
    queryset = Caution.objects.all()
    queryset.delete()