from api.models import Caution

import json

def run():
    # url json 파일 읽어오는 부분
    with open('scripts/caution.json') as json_file:
        data = json.load(json_file)


    try:
        for num in range(len(data['caution_list'])):
            nutrient = data['caution_list'][num]['name']
            caution = data['caution_list'][num]['caution']

            try:
                Caution.objects.filter(name=nutrient)[0]
            except:
                # create(테이블 속성명 = 위에 변수)
                Caution.objects.create(name=nutrient, caution=caution)
    except IndexError:
        pass
