from api.models import BodyType

def run():
    # 체질 추가
    BodyType.objects.create(body_type='열태양')
    BodyType.objects.create(body_type='한태양')

    BodyType.objects.create(body_type='열소음')
    BodyType.objects.create(body_type='한소음')

    BodyType.objects.create(body_type='열소양')
    BodyType.objects.create(body_type='한소양')

    BodyType.objects.create(body_type='열태음')
    BodyType.objects.create(body_type='한태음')


