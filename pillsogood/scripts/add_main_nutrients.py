from api.models import MainNutrient

import json

def run():
    # url json 파일 읽어오는 부분
    with open('scripts/main_nutrients.json') as json_file:
        data = json.load(json_file)

    # 메인 영양소 추가
    try:
        for num in range(23):
            n = data['main_nutrients'][num]['name']

            # 메인 영양소 추가
            MainNutrient.objects.create(name=n)
    except IndexError:
        pass
