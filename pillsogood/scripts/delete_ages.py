from api.models import Age

def run():
    queryset = Age.objects.all()
    queryset.delete()