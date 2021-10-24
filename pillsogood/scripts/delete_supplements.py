from api.models import Supplement

def run():
    queryset = Supplement.objects.all()
    queryset.delete()