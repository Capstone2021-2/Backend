from api.models import GoodForAge
from api.models import Nutrient
import json

def run():
    # url json 파일 읽어오는 부분
    with open('scripts/good_for_age.json') as json_file:
        data = json.load(json_file)

    try:
        for num in range(len(data['age_range_list'])):
            age_range = data['age_range_list'][num]['age_range']
            gender = data['age_range_list'][num]['gender']
            nutrients = data['age_range_list'][num]['nutrient']
            nutrients = nutrients.split(',')

            print(nutrients)

            for nutrient in nutrients:
                nutrient = nutrient.strip(' ')
                nutrient_object = Nutrient.objects.all().get(name=nutrient)
                nutrient_pk = nutrient_object.pk
                # 몸에 좋은 영양소 추가
                GoodForAge.objects.create(age_range=age_range, gender=gender, nutrient_pk=nutrient_pk, nutrient=nutrient)
    except IndexError:
        pass