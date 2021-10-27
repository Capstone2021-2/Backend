from api.models import GoodForOrgan

import json

def run():
    # url json 파일 읽어오는 부분
    with open('scripts/goodfororgan.json') as json_file:
        data = json.load(json_file)

    
    try:
        for num in range(len(data['goodfororgan'])):
            organ = data['goodfororgan'][num]['organ']
            nutrient = data['goodfororgan'][num]['nutrient']

            # 몸에 좋은 영양소 추가
            GoodForOrgan.objects.create(organ=organ, nutrient=nutrient)
    except IndexError:
        pass