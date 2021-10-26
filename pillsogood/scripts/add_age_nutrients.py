from api.models import AgeNutrient

import json

def run():
    # url json 파일 읽어오는 부분
    with open('scripts/nutrient-ages.json') as json_file:
        data = json.load(json_file)

    # 나이 구간은 총 개수는 450개
    try:
        for num in range(450):
            gender = data['age_info'][num]['gender']
            age = data['age_info'][num]['ages']
            nutrient = data['age_info'][num]['nutrient']
            upper = data['age_info'][num]['upper']
            lower = data['age_info'][num]['lower']
            
            # 나이별 영양소 정보 추가
            AgeNutrient.objects.create(gender=gender, ages=age, nutrient=nutrient, upper=upper, lower=lower)
    except IndexError:
        pass

