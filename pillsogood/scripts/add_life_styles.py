from api.models import LifeStyle

import json

def run():
    # url json 파일 읽어오는 부분
    with open('scripts/life_styles_info.json') as json_file:
        data = json.load(json_file)

    try:
        for num in range(len(data['life_styles'])):
            life_style = data['life_styles'][num]['life_style']

            try:
                LifeStyle.objects.filter(life_style=life_style)[0]
            except:
                LifeStyle.objects.create(life_style=life_style)
    except IndexError:
        pass

    