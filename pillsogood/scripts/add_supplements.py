import json
from api.models import Supplement

def run():
    # url json 파일 읽어오는 부분
    with open('scripts/01.json') as json_file:
        data = json.load(json_file)
    try:
        for num in range(int(data['C003']['total_count'])):
            product = data['C003']['row'][num]['PRDLST_NM']  # PRDLIST_NM = 제품명
            company = data['C003']['row'][num]["BSSH_NM"]
            exp_date = data['C003']['row'][num]["POG_DAYCNT"]
            dispos = data['C003']['row'][num]["DISPOS"]
            sug_use = data['C003']['row'][num]["NTK_MTHD"]
            warning = data['C003']['row'][num]["IFTKN_ATNT_MATR_CN"]
            pri_func = data['C003']['row'][num]["PRIMARY_FNCLTY"]
            raw_material = data['C003']['row'][num]["RAWMTRL_NM"]
            tmp_id = data['C003']['row'][num]["-id"]

            if '(주)' in company:
                company = company.replace('(주)', '')
            if '주)' in company:
                company = company.replace('주)', '')
            if '주 )' in company:
                company = company.replace('주 )', '')
            if '(유)' in company:
                company = company.replace('(유)', '')
            if '공장' in company:
                company = company.replace('공장', '')
            if '주식회사' in company:
                company = company.replace('주식회사', '')
            if '음성' in company:
                company = company.replace('음성', '')
            if '금산지점' in company:
                company = company.replace('금산지점', '')
            if '농업회사법인' in company:
                company = company.replace('농업회사법인', '')
            if '포천 제' in company:
                company = company.replace('포천 제', '')
            if '반월' in company:
                company = company.replace('반월', '')
            if '자연건강사업부' in company:
                company = company.replace('자연건강사업부', '')
            if '건강식품사업부문' in company:
                company = company.replace('건강식품사업부문', '')
            if '식품사업부' in company:
                company = company.replace('식품사업부', '')
            if '충주' in company:
                company = company.replace('충주', '')
            if '-제' in company:
                company = company.replace('-제', '')
            
            if '1' in company:
                company = company.replace('1', '')
            if '2' in company:
                company = company.replace('2', '')
            if '3' in company and '360' not in company:
                company = company.replace('3', '')
            if '4' in company:
                company = company.replace('4', '')
            if ',' in company:
                company = company.replace(',', '')
            if ' ' in company:
                company = company.replace(' ', '')

            # 이름이 똑같은 영양제가 있을 수 있음
            try:
                Supplement.objects.filter(name=product)[0]
            except IndexError:
                Supplement.objects.create(
                    name=product, company=company, exp_date=exp_date,
                    dispos=dispos, sug_use = sug_use, warning=warning,
                    pri_func=pri_func, raw_material=raw_material, tmp_id=tmp_id)
            else:
                Supplement.objects.create(
                    name=product, company=company, exp_date=exp_date,
                    dispos=dispos, sug_use = sug_use, warning=warning,
                    pri_func=pri_func, raw_material=raw_material, tmp_id=tmp_id)
    except IndexError:
        pass

