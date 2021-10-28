from api.models import Organ

def run():
    queryset = Organ.objects.all()
    queryset.delete()