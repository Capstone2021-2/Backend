from api.models import BodyType

def run():
    # 체질 추가
    BodyType.objects.create(body_type='금양')
    BodyType.objects.create(body_type='금음')

    BodyType.objects.create(body_type='수양')
    BodyType.objects.create(body_type='수음')

    BodyType.objects.create(body_type='토음')
    BodyType.objects.create(body_type='토양')

    BodyType.objects.create(body_type='목음')
    BodyType.objects.create(body_type='목양')


