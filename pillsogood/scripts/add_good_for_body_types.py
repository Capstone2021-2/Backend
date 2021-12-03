from api.models import GoodForBodyType
from api.models import Nutrient
import json

def run():
    # url json 파일 읽어오는 부분
    with open('scripts/good_for_body_types.json') as json_file:
        data = json.load(json_file)

    try:
        for num in range(len(data['bodytype_list'])):
            bodytype = data['bodytype_list'][num]['bodytype']
            nutrients = data['bodytype_list'][num]['nutrients']
            nutrients = nutrients.split(',')

            for nutrient in nutrients:
                nutrient_object = Nutrient.objects.all().get(name=nutrient)
                nutrient_pk = nutrient_object.pk
                # 체질별 필요한 영양소 추가
                GoodForBodyType.objects.create(bodytype=bodytype, nutrient_pk=nutrient_pk, nutrient=nutrient)
    except IndexError:
        pass