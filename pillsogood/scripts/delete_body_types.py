from api.models import BodyType


def run():
    # 체질 추가
    queryset = BodyType.objects.all()
    queryset.delete()


