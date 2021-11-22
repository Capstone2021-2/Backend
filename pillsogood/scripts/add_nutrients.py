from api.models import Nutrient

import json

cnt = 0
def run():
    # url json 파일 읽어오는 부분
    with open('scripts/nutrients_info.json') as json_file:
        data = json.load(json_file)

    # 뒤에서 부터 0번까지
    try:
        # for num in range(int(data['I2710']['total_count'])-1, -1, -1):
        for num in range(int(data['I2710']['total_count'])):
            prdct_nm = data['I2710']['row'][num]['PRDCT_NM']
            highlimit = data['I2710']['row'][num]['DAY_INTK_HIGHLIMIT']
            lowlimit = data['I2710']['row'][num]['DAY_INTK_LOWLIMIT']
            unit = data['I2710']['row'][num]['INTK_UNIT']
            tmp_id = data['I2710']['row'][num]["-id"]
            search_count = 0

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
            
            

            # print(Nutrient.objects.get(name=prdct_nm)) # 여기서 오류
            try:
                Nutrient.objects.filter(name=prdct_nm)[0]
            except:
                # create(테이블 속성명 = 위에 변수)
                Nutrient.objects.create(name=prdct_nm, upper=highlimit, lower=lowlimit, unit=unit, tmp_id=tmp_id, search_count=search_count)
    except IndexError:
        pass
