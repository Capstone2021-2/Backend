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

            # 이름이 똑같은 영야제가 있을 수 있음
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

