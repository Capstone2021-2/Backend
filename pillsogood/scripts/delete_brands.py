from api.models import Brand

def run():
    queryset = Brand.objects.all()
    queryset.delete()