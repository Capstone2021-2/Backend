from api.models import Organ

import json


def run():
    # url json 파일 읽어오는 부분
    with open('scripts/goodfororgan.json') as json_file:
        data = json.load(json_file)


    try:
        for num in range(len(data['goodfororgan'])):
            organ = data['goodfororgan'][num]['organ']

            try:
                Organ.objects.filter(organ=organ)[0]
            except:
                # create(테이블 속성명 = 위에 변수)
                Organ.objects.create(organ=organ)
    except IndexError:
        pass
