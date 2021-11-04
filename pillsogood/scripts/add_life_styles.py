from api.models import LifeStyle

import json

def run():
    # url json 파일 읽어오는 부분
    with open('scripts/life_styles_info.json') as json_file:
        data = json.load(json_file)

    try:
        for num in range(len(data['life_styles'])):
            life_style = data['life_styles'][num]['life_style']

            # 몸에 좋은 영양소 추가
            LifeStyle.objects.create(life_style=life_style)
    except IndexError:
        pass