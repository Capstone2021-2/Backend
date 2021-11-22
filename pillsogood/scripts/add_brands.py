import json
from api.models import Brand

def run():
    # url json 파일 읽어오는 부분
    with open('scripts/01.json') as json_file:
        data = json.load(json_file)
    

    for num in range(len(data['C003']['row'])):
        id = data['C003']['row'][num]['-id']
        company = data['C003']['row'][num]["BSSH_NM"]

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

        try:
            Brand.objects.filter(name=company)[0]
        except IndexError:
            Brand.objects.create(name=company)
        else:
            pass

