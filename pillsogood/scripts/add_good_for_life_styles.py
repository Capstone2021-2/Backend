from api.models import GoodForLifeStyle

import json

def run():
    # url json 파일 읽어오는 부분
    with open('scripts/life_styles_info.json') as json_file:
        data = json.load(json_file)

    try:
        for num in range(len(data['life_styles'])):
            lifestyle = data['life_styles'][num]['life_style']
            nutrient = data['life_styles'][num]['nutrient']

            # 몸에 좋은 영양소 추가
            GoodForLifeStyle.objects.create(life_style=lifestyle, nutrient=nutrient)
    except IndexError:
        pass