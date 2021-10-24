from api.models import Nutrient

import json
import requests

cnt = 0
def run():
    # url json 파일 읽어오는 부분
    url = requests.get('http://openapi.foodsafetykorea.go.kr/api/3c253c418f214752a6d5/I2710/json/1/400')
    text = url.text
    data = json.loads(text)

    # 뒤에서 부터 0번까지
    for num in range(int(data['I2710']['total_count'])-1, -1, -1):
        prdct_nm = data['I2710']['row'][num]['PRDCT_NM']
        highlimit = data['I2710']['row'][num]['DAY_INTK_HIGHLIMIT']
        lowlimit = data['I2710']['row'][num]['DAY_INTK_LOWLIMIT']
        unit = data['I2710']['row'][num]['INTK_UNIT']

        # New라는 부분 없애기
        if 'New' in prdct_nm:
            prdct_nm = prdct_nm.replace('New', '')
        index = prdct_nm.rfind('제')
        # 불필요한 괄호 없애기
        if index != -1:
            tmp = prdct_nm[index-1:]
            prdct_nm = prdct_nm.replace(tmp, '')

        if highlimit == '':
            highlimit = 0
        if lowlimit == '':
            lowlimit = 0
        try:
            Nutrient.objects.filter(name=prdct_nm)[0]
        except IndexError:
            Nutrient.objects.create(name=prdct_nm, upper=highlimit, lower=lowlimit, unit=unit)
            

        
    # print(Nutrient.objects.filter(name='비오틴')[0])

