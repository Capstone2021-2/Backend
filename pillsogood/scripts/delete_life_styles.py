from api.models import LifeStyle


def run():
    # 체질 추가
    queryset = LifeStyle.objects.all()
    queryset.delete()


