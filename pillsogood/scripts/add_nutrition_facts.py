from api.models import NutritionFact
from api.models import Nutrient, Supplement
import json
import re
from parse import search



def run():
    with open('scripts/01.json') as json_file:
        data = json.load(json_file)

    cnt = 0
    try:
        for num in range(955):  # 데이터 몇 개 받아오는지 지정
            product = data['C003']['row'][num]['PRDLST_NM']  # PRDLIST_NM = 제품명
            # print('------------------------------------')
            # print(product)
            # print('------------------------------------')
            contents = data['C003']['row'][num]['STDR_STND'].split('\n')  # 함량 목록(STDR_STND) split 함수 사용해서 추출
            tmp_id_sup = data['C003']['row'][num]["-id"]  # json 파일 id를 사용해서 manytomany할 때 참조 객체 찾아야함.

            cnt += 1
            # 여러 함량들 중 함량 하나씩 파싱하는 부분
            for content in contents:
                # 무슨 함량인지
                c_name = None
                if c_name is None:
                    c_name = search('총(-)-{} : ', content)  # 총(-)-Hydorxycitric acid
                if c_name is None:
                    c_name = search(')총 (-)-{} : ', content)  # )총 (-)-Hydorxycitric acid
                if c_name is None:
                    c_name = search('. 총 {} :', content)  # . 총 이름 :

                if c_name is None:
                    c_name = search(') {}(%) : ', content)  # 2) 이름(%): 형식
                if c_name is None:
                    c_name = search(') {} : ', content)  # 2) 이름 : 형식
                if c_name is None:
                    c_name = search('){} : ', content)  # 2)이름 : 형식
                if c_name is None:
                    c_name = search(') {}: ', content)  # 2) 이름: 형식
                if c_name is None:
                    c_name = search('. {}(%) : ', content)  # 2. 이름(%) : 형식
                if c_name is None:
                    c_name = search('.{} : ', content)  # 2.이름 : 형식
                if c_name is None:
                    c_name = search('. {} : ', content)  # 2. 이름 : 형식
                if c_name is None:
                    c_name = search('. {}: ', content)  # 2. 이름: 형식
                if c_name is None:
                    c_name = search('{} : ', content)  # 특수문자숫자이름 : 형식
                if c_name is None:
                    c_name = search(' {} : ', content)  # 특수문자숫자 이름 : 형식
                if c_name is None:
                    c_name = search('{}: ', content)  # 특수문자숫자이름: 형식
                    # if c_name is not None:
                    #     print(c_name.fixed[0])

                # 유해 물질이 들어가게 되면 빼주기
                if c_name is not None and ('납' in c_name.fixed[0] or
                                        '중금속' in c_name.fixed[0] or
                                        '카페인' in c_name.fixed[0] or
                                        '비소' in c_name.fixed[0] or
                                        '수은' in c_name.fixed[0] or
                                        '카드뮴' in c_name.fixed[0] or
                                        '깅콜릭산' in c_name.fixed[0] or
                                        '성상' in c_name.fixed[0] or
                                        c_name.fixed[0].startswith('1') or
                                        '대장균군' in c_name.fixed[0] or
                                        '초산에틸' in c_name.fixed[0] or
                                        '헥산' in c_name.fixed[0] or
                                        '잔류용매' in c_name.fixed[0] or
                                        '세균' in c_name.fixed[0]):
                    c_name = None

                if c_name is not None and '프로바이오틱스' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '프로바이오틱스'
                elif c_name is not None and '아세틸' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = 'NAG(엔에이지, N-아세틸글루코사민, N-Acetylglucosamine)'

                # 영양소 이름 형식 맞춰주기
                # 비타민 이름 띄어쓰기 맞춰주기
                elif c_name is not None and '비타민A' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '비타민 A'
                elif c_name is not None and '비타민 A' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '비타민 A'
                elif c_name is not None and '비타민B2' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '비타민 B2'
                elif c_name is not None and '비타민 B2' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '비타민 B2'
                elif c_name is not None and '비타민B6' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '비타민 B6'
                elif c_name is not None and '비타민 B6' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '비타민 B6'
                elif c_name is not None and '비타민B1' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '비타민 B1'
                elif c_name is not None and '비타민 B1' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '비타민 B1'
                elif c_name is not None and '비타민12' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '비타민 B12'
                elif c_name is not None and '비타민 12' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '비타민 B12'
                elif c_name is not None and '비타민C' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '비타민 C'
                elif c_name is not None and '비타민 C' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '비타민 C'
                elif c_name is not None and '비타민D' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '비타민 D'
                elif c_name is not None and '비타민 D' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '비타민 D'
                elif c_name is not None and '비타민E' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '비타민 E'
                elif c_name is not None and '비타민 E' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '비타민 E'
                elif c_name is not None and '비타민K' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '비타민 K'
                elif c_name is not None and '비타민 K' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '비타민 K'

                elif c_name is not None and '아스타잔' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '헤마토코쿠스 추출물'
                elif c_name is not None and '아스타진' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '헤마토코쿠스 추출물'
                elif c_name is not None and '루테인' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '루테인지아잔틴복합추출물'
                elif c_name is not None and '지아잔틴' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '루테인지아잔틴복합추출물'
                elif c_name is not None and '요오드' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '요오드'

                elif c_name is not None and '나이아신' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '나이아신'
                elif c_name is not None and '판토텐산' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '판토텐산'
                elif c_name is not None and '아연' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '아연'
                elif c_name is not None and '엽산' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '엽산'
                elif c_name is not None and '망간' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '망간'
                elif c_name is not None and '마그네슘' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '마그네슘'
                elif c_name is not None and '코엔자임Q10' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '코엔자임Q10'
                elif c_name is not None and '셀레늄' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '셀레늄'
                elif c_name is not None and '셀렌' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '셀레늄'
                elif c_name is not None and '프락토올리고당' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '프락토올리고당'
                elif c_name is not None and '소포리코사이드' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '회화나무열매추출물'
                elif c_name is not None and '진센노사이드' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '홍삼'
                elif c_name is not None and '진세노사이드' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '홍삼'
                elif c_name is not None and '플라보노이드' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '프로폴리스추출물'
                elif c_name is not None and '철' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '철'
                elif c_name is not None and '구리' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '구리'
                elif c_name is not None and 'EPA' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = 'EPA와 DHA의 합'
                elif c_name is not None and '안트라' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '안트라퀴논계화합물(무수바바로인으로서)'
                elif c_name is not None and 'HCA' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '가르시니아캄보지아 추출물'
                elif c_name is not None and 'Hydroxycitric' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '가르시니아캄보지아 추출물'
                elif c_name is not None and '키토' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '키토산'
                elif c_name is not None and '차전자피' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '차전자피식이섬유'
                elif c_name is not None and '식이섬유' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '식이섬유'
                elif c_name is not None and '포스파티' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '포스파티딜세린'
                elif c_name is not None and '비오틴' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '비오틴'
                elif c_name is not None and '카테킨' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '녹차추출물'
                elif c_name is not None and 'Quercetin' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '시서스추출물'
                elif c_name is not None and '히알루론' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '히알루론산'
                elif c_name is not None and '옥타코사놀' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '옥타코사놀 함유 유지'
                elif c_name is not None and '칼슘' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '칼슘'
                elif c_name is not None and '칼슘' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '칼슘'
                elif c_name is not None and 'MSM' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '엠에스엠(MSM, Methyl sulfonylmethane, 디메틸설폰)'
                elif c_name is not None and '엠에스엠' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '엠에스엠(MSM, Methyl sulfonylmethane, 디메틸설폰)'
                elif c_name is not None and '플라보' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '은행잎 추출물'
                elif c_name is not None and '폴라보' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '은행잎 추출물'
                elif c_name is not None and '플라포' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '은행잎 추출물'
                elif c_name is not None and '폴라포' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '은행잎 추출물'
                elif c_name is not None and '실리마린' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '밀크씨슬(카르두스 마리아누스) 추출물'

                elif c_name is not None and '로르산' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '쏘팔메토 열매 추출물'
                elif c_name is not None and '베타카로틴' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '베타카로틴'
                elif c_name is not None and '베타글루칸' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '영지버섯 자실체 추출물'
                elif c_name is not None and '테아닌' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '테아닌'
                elif c_name is not None and '다당체' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '알로에 겔'
                elif c_name is not None and '단백질' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '단백질'

                elif c_name is not None and '감마리놀렌산' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '감마리놀렌산 함유 유지'
                elif c_name is not None and '대두이소' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '대두이소플라본'

                elif c_name is not None and '로사빈' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '홍경천 추출물'
                elif c_name is not None and 'Cycloalliin' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '유산균발효마늘추출물'
                elif c_name is not None and '디엑콜' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '감태추출물'
                elif c_name is not None and '폴리페놀' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '포도씨 효소분해 추출 분말'
                elif c_name is not None and '글루코실' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '쌀겨추출물'
                elif c_name is not None and 'Gly-Pro-Val-Gly-Pro-Ser' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '피쉬 콜라겐펩타이드'
                elif c_name is not None and '공액리놀레산' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '공액리놀레산'

                elif c_name is not None and 'carnosic' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '로즈마리자몽추출복합물(Nutroxsun)'
                elif c_name is not None and '알파에스' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '유단백가수분해물'
                elif c_name is not None and '뮤코다당' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '뮤코다당.단백'
                elif c_name is not None and '엽록소' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '스피루리나'
                elif c_name is not None and '안토시아' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '빌베리 추출물'
                elif c_name is not None and '락추로스' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '락추로스 파우더(Lactulose Powder)'

                elif c_name is not None and '락토페린' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '리스펙타(Respecta®) 프로바이오틱스'
                elif c_name is not None and '크롬' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '크롬'
                elif c_name is not None and '코로솔산' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '바나바잎 추출물'
                elif c_name is not None and '자일로' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '자일로올리고당'
                elif c_name is not None and '포스콜린' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '콜레우스포스콜리추출물'
                elif c_name is not None and '카르니틴' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = 'L-카르니틴 타르트레이트'
                elif c_name is not None and 'sakei' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = 'Lactobacillus sakei Probio65'
                elif c_name is not None and '데커신' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '참당귀 추출분말(Nutragen)'
                elif c_name is not None and 'Chlorogenic' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '그린커피빈추출물'
                elif c_name is not None and 'Damulin' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '돌외잎주정추출분말'
                elif c_name is not None and '폴리감마' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '폴리감마글루탐산'
                elif c_name is not None and '식물스타놀' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '식물스타놀 에스테르'
                elif c_name is not None and 'dipeptide' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '저분자콜라겐펩타이드NS'
                elif c_name is not None and '갈산' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '보이차추출물'
                elif c_name is not None and 'Ellagic' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '석류농축분말'
                elif c_name is not None and '엘라그산' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '석류농축분말'
                elif c_name is not None and 'Coumaric' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '강황 추출물(터마신)'
                elif c_name is not None and '몰리브덴' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '몰리브덴'
                elif c_name is not None and '풋사과' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '풋사과추출물 애플페논(Applephenon)'
                elif c_name is not None and 'Hyperoside' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '로즈힙분말'
                elif c_name is not None and 'Vitexin' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '호로파종자추출물(Testofen)'
                elif c_name is not None and 'Luteolin-7' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '차즈기추출물'
                elif c_name is not None and '오리자놀' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '미강주정추출물'
                elif c_name is not None and 'Secoxyloganin' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '인동덩굴꽃봉오리추출물(그린세라-F)'
                elif c_name is not None and '벤질헥사' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '마카 젤라틴화 분말'
                elif c_name is not None and '틸리아닌' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '배초향 추출물(Agatri®)'
                elif c_name is not None and '클로로겐산' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '해국추출물'
                elif c_name is not None and 'aminobutyric' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '유산균 발효 다시마추출물'
                elif c_name is not None and '나토균배양분말' in c_name.fixed[0]:
                    c_name.fixed = list(c_name.fixed)
                    c_name.fixed[0] = '나토균배양분말'



                # 함량 얼마나 들어 있는지
                c_amount = None
                if c_amount is None:
                    c_amount = search(': 표시량 ({}/', content)  # : 표시량 (1.5 mg/200 mg) 형식
                if c_amount is None:
                    c_amount = search(': 표시량 이상({} /', content)    # : 표시량 이상(100,000,000 CFU / 5g) 형식
                if c_amount is None:
                    c_amount = search(': 표시량 이상 (표시량 : {} /', content)  # : 표시량 이상(표시량 : 3~~ CFU /) 형식
                if c_amount is None:
                    c_amount = search('표시량 {} /', content)  # 표시량 1.5g / 200mg 형식
                if c_amount is None:
                    c_amount = search('표시량({}/', content)  # 표시량(1.5g/200mg) 형식
                if c_amount is None:
                    c_amount = search('(표시량: {} /', content) # (표시량: 1,000mg / 1,400mg) 형식
                if c_amount is None:
                    c_amount = search('(표시량 : {} /', content)  # 표시량 : 1.5g / 200mg 형식
                if c_amount is None:
                    c_amount = search(': 표시량[{} /', content)  # : 표시량[200 mg / 형식
                if c_amount is None:
                    c_amount = search('표시량 이상- 프로바이오틱스 수: {}/', content)   # 표시량 이상- 프로바이오틱스 수: 10,000,000 CFU/g 이상 형식
                if c_amount is None:
                    c_amount = search(': 표시량 {}/', content)  # : 표시량 ｛1.4mg/ 형식 (잘안됨)
                if c_amount is None:
                    c_amount = search(' : {}/', content)  # : 1,000mg/100g 형식



                supplement_obj = Supplement.objects.get(tmp_id=tmp_id_sup)

                # 함량 이름과 양 둘 다 유효할 경우만 print
                if c_name is not None and c_amount is not None:
                    nutrient_obj = Nutrient.objects.get(name=c_name.fixed[0])  # 영양소 성분 이름으로 찾기
                    if '프로바이오틱스' in c_name.fixed[0]:
                        # print(
                        #     c_name.fixed[0],
                        #     c_amount.fixed[0].replace('CFU', '').replace(' ', '').replace(',', '').replace('cfu', ''))

                        # DB에 저장하는 부분
                        amount= c_amount.fixed[0].replace('CFU', '').replace(' ', '').replace(',', '').replace('cfu', '')
                        NutritionFact.objects.create(supplement=supplement_obj, nutrient=nutrient_obj, amount=amount)
                    else:
                        # 오류 찾기용 print
                        # print(c_name)  # 영양소 이름이 잘못되었나?
                        # print(c_amount)  # 양이 잘못되었나?
                        floats = re.findall(r"[-+]?\d*[.,]\d+|\d+", c_amount.fixed[0])
                        # print(c_name.fixed[0], floats[0].replace(',', ''))

                        # DB에 저장하는 부분
                        amount= floats[0].replace(',', '')
                        NutritionFact.objects.create(supplement=supplement_obj, nutrient=nutrient_obj, amount=amount)

            # print('\n')
    except IndexError:
        pass