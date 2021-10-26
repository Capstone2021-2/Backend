from api.models import Age

import json

def run():
    # url json 파일 읽어오는 부분
    with open('scripts/nutrient-ages.json') as json_file:
        data = json.load(json_file)

    # 나이 구간은 총 9개
    try:
        for num in range(9):
            age = data['age_info'][num]['ages']

            # 나이 추가
            Age.objects.create(age_range=age)
    except IndexError:
        pass

