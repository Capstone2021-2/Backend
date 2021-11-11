# from django.shortcuts import render

from django.utils.regex_helper import contains
from django.views.decorators.csrf import csrf_exempt
from rest_framework import views
from .models import *
from .serializer import *
from rest_framework import viewsets, mixins, generics
from django.http.response import Http404
from django.db.models import query

from django.http import HttpResponseRedirect
from rest_framework import permissions, status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
import django_filters.rest_framework

#--------------------------클래스형 view--------------------------
class MainNutrientViewSet(viewsets.ModelViewSet):
    queryset = MainNutrient.objects.all()
    serializer_class = MainNutrientSerializer
    permission_classes = [permissions.AllowAny]

# APIView는 클래스형 view를 사용할 때 사용
class NutrientViewSet(viewsets.ModelViewSet):
    queryset = Nutrient.objects.all()
    serializer_class = NutrientSerializer
    permission_classes = [permissions.AllowAny]
    # permission_classes = [permissions.IsAuthenticated]

class NutrientDetail(APIView):
    permission_classes = [permissions.AllowAny]

    def get_object(self, nutrient):
        print("이름 출력:", nutrient)
        try:
            return Nutrient.objects.get(name=nutrient)
        except Nutrient.DoesNotExist:
            raise Http404
    def get(self, request, nutrient, format=None):
        nutrient = self.get_object(nutrient)
        serializer = NutrientSerializer(nutrient)
        return Response(serializer.data)
        

class SupplementViewSet(viewsets.ModelViewSet):
    queryset = Supplement.objects.all().order_by('name')
    serializer_class = SupplementSerializer
    permission_classes = [permissions.AllowAny]

class SupplementDetail(APIView):
    permission_classes = [permissions.AllowAny]

    def get_object(self, name):
        try:
            return Supplement.objects.get(name=name)
        except Supplement.DoesNotExist:
            raise Http404
    def get(self, request, name, format=None):
        supplement = self.get_object(name)  # get_object()를 통해 client가 전달해준 name과 일치하는 영양제 가져옴.
        serializer = SupplementSerializer(supplement)
        return Response(serializer.data)

# 복용 중인 영양제 전체
class TakingSupplementsViewSet(viewsets.ModelViewSet):
    queryset = TakingSupplements.objects.all()
    serializer_class = TakingSupplementsSerializer
    permission_classes = [permissions.AllowAny]


    # POST 부분
    def create(self, request, *args, **kwargs):
        supple_pk = request.data['supplement_pk'][0] # 사용자가 보내준 supplement_pk 추출
        supplement = Supplement.objects.get(pk=supple_pk)  # supple_pk 값으로 supplement 객체 가져오기

        # 현재 복용 중인 수 늘려주기
        supplement.taking_num += 1
        supplement.save()
        return super().create(request, *args, **kwargs)

    # DELETE 부분 (TakingSupplements pk 값으로만 삭제)
    def destroy(self, request, *args, **kwargs):

        supplement_pk = self.get_object().supplement_pk.pk

        # 현재 복용 중인 수 줄여주기
        supplement = Supplement.objects.get(pk=supplement_pk)
        if supplement.taking_num > 0:
            supplement.taking_num -= 1
        supplement.save()

        return super().destroy(request, *args, **kwargs)


# user pk로 복용중인 영양제 가져오기 & 삭제 하기

class TakingSupplementsUser(APIView):
    permission_classes = [permissions.AllowAny]

    def get_object(self, user_pk):
        try:
            return TakingSupplements.objects.all().filter(user_pk=user_pk)  # 여러 데이터 전달하기 위해
        except TakingSupplements.DoesNotExist:
            raise Http404
    def get(self, request, user_pk, format=None):
        taking_supplements = self.get_object(user_pk)
        serializer =TakingSupplementsSerializer(taking_supplements, many=True)  # 결과가 여러개 나오기 때문에 many = True
        return Response(serializer.data)

    # user_pk와 supplement_pk로 삭제
    def delete(self, request, **kwargs):
        if kwargs.get('user_pk') is None or kwargs.get('supplement_pk') is None:
            return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)
        else:
            
            taking_supplements_objects = TakingSupplements.objects.all().filter(user_pk=kwargs.get('user_pk'))  # 여러 데이터 전달하기 위해
            taking_supplements_objects = taking_supplements_objects.filter(supplement_pk=kwargs.get('supplement_pk'))
            print(taking_supplements_objects)
            taking_supplements_objects.delete()

            # 현재 복용 중인 수 줄여주기
            supplement = Supplement.objects.get(pk=kwargs.get('supplement_pk'))
            if supplement.taking_num > 0:
                supplement.taking_num -= 1
            supplement.save()
            return Response("Delete Success", status=status.HTTP_200_OK)

    

class TmpBestSupplements(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, name, format=None ):
        supplement = Supplement.objects.all().order_by('-avg_rating')[:10]
        serializer = SupplementSerializer(supplement, many=True)
        return Response(serializer.data)

# 함유 영양소 전체
class NutritionFactViewSet(viewsets.ModelViewSet):
    queryset = NutritionFact.objects.all()
    serializer_class = NutritionFactSerializer
    permission_classes = [permissions.AllowAny]


# 함유 영양소로 영양제 검색
class NutritionFactNutrientToSupplement(APIView):
    permission_classes = [permissions.AllowAny]

    def get_object(self, nutrient_pk):
        print("이름 출력:", nutrient_pk)
        try:
            return NutritionFact.objects.all().filter(nutrient=nutrient_pk)  # 여러 데이터 전달하기 위해
        except NutritionFact.DoesNotExist:
            raise Http404
    def get(self, request, nutrient_pk, format=None):
        nutrition = self.get_object(nutrient_pk)
        serializer = NutritionFactSerializer(nutrition, many=True)  # 결과가 여러개 나오기 때문에 many = True
        return Response(serializer.data)

# 영양제로 함유 여양소 검색
class NutritionFactSupplementToNutrient(APIView):
    permission_classes = [permissions.AllowAny]

    def get_object(self, supplement_pk):
        try:
            return NutritionFact.objects.all().filter(supplement=supplement_pk)  # 여러 데이터 전달하기 위해
        except NutritionFact.DoesNotExist:
            raise Http404
    def get(self, request, supplement_pk, format=None):
        supplement = self.get_object(supplement_pk)
        serializer = NutritionFactSerializer(supplement, many=True)  # 결과가 여러개 나오기 때문에 many = True
        return Response(serializer.data)

class OrganViewSet(viewsets.ModelViewSet):
    queryset = Organ.objects.all()
    serializer_class = OrganSerializer
    permission_classes = [permissions.AllowAny]

class GoodForOrganViewSet(viewsets.ModelViewSet):
    queryset = GoodForOrgan.objects.all()
    serializer_class = GoodForOrganSerializer
    permission_classes = [permissions.AllowAny]

class GoodForOrganDetail(APIView):
    permission_classes = [permissions.AllowAny]

    # 예) 클라이언트가 '간'에 좋은 영양소를 요청하면
    # organ에 '간'이 올 것임.
    def get_object(self, organ):
        print("장기 이름 출력:", organ)
        try:
            return GoodForOrgan.objects.all().filter(organ=organ)  # organ 이름으로 filtering
        except GoodForOrgan.DoesNotExist:
            raise Http404
    def get(self, request, organ, format=None):
        nutrient = self.get_object(organ)
        serializer = GoodForOrganSerializer(nutrient, many=True)  # 해당 organ에 좋은 영양소 결과가 여러개 나오기 때문에 many = True
        return Response(serializer.data)  # 

            

class AgeNutrientViewSet(viewsets.ModelViewSet):
    queryset = AgeNutrient.objects.all()
    serializer_class = SupplementSerializer
    permission_classes = [permissions.AllowAny]

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.AllowAny]

class BrandToSupplements(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, brand, format=None):
        supplement_list = Supplement.objects.all().filter(company=brand)  # organ에 좋은 영양소 리스트
        # print('리스티', supplement_list)
        # tmp_list = []  # serializer 하기 전에 data 있는지 없는지 확인하기 위한 용도
        return_list = []
        # print(nutrient_list)
        for num in range(supplement_list.count()):
            try:
                supplement_obj = supplement_list[num]
                # print('옵젝', supplement_obj)
                serializer = SupplementSerializer(supplement_obj)
                return_list.append(serializer.data)
                        
            except IndexError:
                pass
        
        return Response(return_list)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    # custom 
    def create(self, request):
        request.data._mutable = True
        supple_pk = request.data['supplement_pk'][0]
        # print(supple_pk)
        rating = int(request.data['rating'][0])
        user_pk = request.data['user_pk'][0]  # User의 나이, 키, 몸무게르 획득할 수 있음.
        user_object = User.objects.get(pk=user_pk)  # User 객체 가져오기

        age = user_object.age  # 나이
        bodytype = user_object.body_type  # 체질
        height = user_object.height  # 키
        weight = user_object.weight  # 몸무게

        # request.data 값 추가해주기
        request.data.__setitem__('age_pk', age.pk)  # age pk 값 추가
        request.data.__setitem__('bodytype_pk', bodytype.pk)  # body_type pk 값 추가
        request.data.__setitem__('height', height)  # age pk 값 추가
        request.data.__setitem__('weight', weight)  # age pk 값 추가


        supplement = Supplement.objects.get(pk=supple_pk)
        # 평균 평점 수정과 리뷰 수 늘려주기
        avg_rating = (supplement.review_num * supplement.avg_rating + rating) / (supplement.review_num + 1)
        avg_rating = round(avg_rating, 2)
        supplement.avg_rating = avg_rating
        supplement.review_num += 1
        supplement.save()
        return super().create(request)


    def destroy(self, request, *args, **kwargs):
        supplement_pk = self.get_object().supplement_pk.pk
        rating = self.get_object().rating

        # 평균 평점 수정과 리뷰 수 줄여주기
        supplement = Supplement.objects.get(pk=supplement_pk)

        if (supplement.review_num-1) > 0:
            avg_rating = (supplement.review_num * supplement.avg_rating - rating) / (supplement.review_num - 1)
            avg_rating = round(avg_rating, 2)
            supplement.avg_rating = avg_rating
            supplement.review_num -= 1
        elif (supplement.review_num-1)  == 0:
            supplement.avg_rating = 0
            supplement.review_num -= 1
        else:
            return Response("Nothing to delete", status=status.HTTP_400_BAD_REQUEST)
        supplement.save()
        return super().destroy(request, *args, **kwargs)



class ReviewUser(APIView):
    permission_classes = [permissions.AllowAny]

    def get_object(self, user_pk):
        try:
            return Review.objects.all().filter(user_pk=user_pk)  # user_pk로 리뷰 filtering
        except Review.DoesNotExist:
            raise Http404

    def get(self, request, user_pk, format=None):
        review = self.get_object(user_pk)
        serializer = ReviewSerializer(review, many=True)  # User 한 명이 여러 리뷰를 남겼을 수 있기 떄문에 many = True
        return Response(serializer.data)

    # user_pk와 supplement_pk로 리뷰 삭제
    def delete(self, request, **kwargs):
        if kwargs.get('user_pk') is None or kwargs.get('supplement_pk') is None:
            return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)
        else:
            review_objects= Review.objects.all().filter(user_pk=kwargs.get('user_pk')) 
            review_objects = review_objects.filter(supplement_pk=kwargs.get('supplement_pk'))
            rating = review_objects[0].rating
            print(rating)
            review_objects.delete()

            # 현재 복용 중인 수 줄여주기
            supplement = Supplement.objects.get(pk=kwargs.get('supplement_pk'))
            if (supplement.review_num-1) > 0:
                avg_rating = (supplement.review_num * supplement.avg_rating - rating) / (supplement.review_num - 1)
                avg_rating = round(avg_rating, 2)
                supplement.avg_rating = avg_rating
                supplement.review_num -= 1
            elif (supplement.review_num-1)  == 0:
                supplement.avg_rating = 0
                supplement.review_num -= 1
            else:
                return Response("Nothing to delete", status=status.HTTP_400_BAD_REQUEST)
            supplement.save()
            return Response("Delete Success", status=status.HTTP_200_OK)


class ReviewSupplement(APIView):
    permission_classes = [permissions.AllowAny]
    def get_object(self, supplement_pk):
        try:
            return Review.objects.all().filter(supplement_pk=supplement_pk)  # supplement_pk로 리뷰 filtering
        except Review.DoesNotExist:
            raise Http404
    def get(self, request, supplement_pk, format=None):
        review = self.get_object(supplement_pk)
        serializer = ReviewSerializer(review, many=True)  # 영양제에 여러 리뷰가 있기 때문에 many = True
        return Response(serializer.data)
    
class AgeViewSet(viewsets.ModelViewSet):
    queryset = Age.objects.all()
    serializer_class = AgeSerializer
    permission_classes = [permissions.AllowAny]

class BodyTypeViewSet(viewsets.ModelViewSet):
    queryset = BodyType.objects.all()
    serializer_class = BodyTypeSerializer
    permission_classes = [permissions.AllowAny]

class LifeStyleViewSet(viewsets.ModelViewSet):
    queryset = LifeStyle.objects.all()
    serializer_class = LifeStyleSerializer
    permission_classes = [permissions.AllowAny]

class GoodForLifeStyleViewSet(viewsets.ModelViewSet):
    queryset = GoodForLifeStyle.objects.all()
    serializer_class = GoodForLifeStyleSerializer
    permission_classes = [permissions.AllowAny]

class GoodForLifeStyleDetail(APIView):
    permission_classes = [permissions.AllowAny]

    # 예) 클라이언트가 '공부에 시달리는 수험생 '에 좋은 영양소를 요청하면
    # life_style에 '공부에 시달리는 수험생'이 올 것임.
    def get_object(self, life_style):
        try:
            return GoodForLifeStyle.objects.all().filter(life_style=life_style)  # life_style 이름으로 filtering
        except GoodForOrgan.DoesNotExist:
            raise Http404
    def get(self, request, life_style, format=None):
        nutrient = self.get_object(life_style)
        serializer = GoodForLifeStyleSerializer(nutrient, many=True)  # 해당 organ에 좋은 영양소 결과가 여러개 나오기 때문에 many = True
        return Response(serializer.data)


class LifeStyleToSupplements(APIView):
    permission_classes = [permissions.AllowAny]

    return_list = []
    tmp_list = []  # serializer 하기 전에 data 있는지 없는지 확인하기 위한 용도
    life_style =''  # search_nutrition_facts에서 더 세분화된 검색 결과를 제공하기 위해 만듦
    # 주요 기능으로 검색   
    def search_pri_func(self, keyword):
        pri_func = Supplement.objects.all().filter(pri_func__icontains=keyword)
        for i in range(pri_func.count()):
            supplement_pk = pri_func[i]
            have = False

            # for item in self.tmp_list:   # 위에서 추가된 값들과 중복되는지 확인
            #     if supplement_pk == item:
            #         have = True

            if not have:
                serializer = SupplementSerializer(supplement_pk)
                self.return_list.append(serializer.data)
                self.tmp_list.append(supplement_pk)

    # 영양제 이름으로 검색
    def search_prd_name(self, keyword):
        pri_func = Supplement.objects.all().filter(name__icontains=keyword)

        for i in range(pri_func.count()):
            supplement_pk = pri_func[i]
            have = False

            for item in self.tmp_list:   # 위에서 추가된 값들과 중복되는지 확인
                if supplement_pk == item:
                    have = True

            if not have:
                serializer = SupplementSerializer(supplement_pk)
                self.return_list.append(serializer.data)
                self.tmp_list.append(supplement_pk)

    # raw_material 이름으로 검색
    def search_raw_material(self, keyword):
        pri_func = Supplement.objects.all().filter(raw_material__icontains=keyword)

        for i in range(pri_func.count()):
            supplement_pk = pri_func[i]
            have = False

            for item in self.tmp_list:   # 위에서 추가된 값들과 중복되는지 확인
                if supplement_pk == item:
                    have = True

            if not have:
                serializer = SupplementSerializer(supplement_pk)
                self.return_list.append(serializer.data)
                self.tmp_list.append(supplement_pk)

    # 성분 함유량으로 검색
    def search_nutrition_facts(self, keyword):
        nutrient = Nutrient.objects.filter(name=keyword)
        nutrient_pk = nutrient[0].pk  # 칼슘의 pk 값은 20임.

        # 일정량 이상 많이 들은 영양제만 추출하기 위함.
        if keyword=='칼슘':
            pri_func = NutritionFact.objects.all().filter(nutrient=nutrient_pk).filter(amount__gt=499)
        elif keyword=='철':
            pri_func = NutritionFact.objects.all().filter(nutrient=nutrient_pk).filter(amount__gt=14)
        elif keyword=='은행잎 추출물':
            pri_func = NutritionFact.objects.all().filter(nutrient=nutrient_pk)
        elif keyword=='은행잎 추출물' and self.life_style == '공부에 시달리는 수험생':
            pri_func = NutritionFact.objects.all().filter(nutrient=nutrient_pk).filter(amount_gt=28)
        elif keyword=='비타민 D':
            pri_func = NutritionFact.objects.all().filter(nutrient=nutrient_pk).filter(amount__gt=14)
        elif keyword=='엽산' and self.life_style == '영양보충에 특히 신경 써야하는 임산부':
            pri_func = NutritionFact.objects.all().filter(nutrient=nutrient_pk).filter(amount__gt=599)
        elif keyword=='EPA와 DHA의 합':
            pri_func = NutritionFact.objects.all().filter(nutrient=nutrient_pk).filter(amount__gt=700)
    

        # print(pri_func)

        if keyword=='엽산' and self.life_style == '영양보충에 특히 신경 써야하는 임산부':
            vitaminA = Nutrient.objects.filter(name='비타민 A')[0].pk
            vitaminD = Nutrient.objects.filter(name='비타민 D')[0].pk
            for i in range(pri_func.count()):
                supplement_pk = pri_func[i].supplement
                filter_A = NutritionFact.objects.all().filter(supplement=supplement_pk).filter(nutrient=vitaminA).filter(amount__gt=999)
                filter_D = NutritionFact.objects.all().filter(supplement=supplement_pk).filter(nutrient=vitaminD).filter(amount__gt=19)
                have = False

                if filter_A.count() != 0:
                    have = True
                    # print('filter A:', filter_A)

                if have == False and filter_D.count() != 0:
                    have = True
                    # print('filter D:', filter_D)

                if not have:
                    serializer = SupplementSerializer(supplement_pk)
                    self.return_list.append(serializer.data)
                    self.tmp_list.append(supplement_pk)
                
        else:
            for i in range(pri_func.count()):
                supplement_pk = pri_func[i].supplement
                # print('supplement pk: ', supplement_pk)
                have = False

                for item in self.tmp_list:   # 위에서 추가된 값들과 중복되는지 확인
                    if supplement_pk == item:
                        have = True

                if not have:
                    serializer = SupplementSerializer(supplement_pk)
                    self.return_list.append(serializer.data)
                    self.tmp_list.append(supplement_pk)

    def get(self, request, life_style, format=None):
        good_nutrients_list = GoodForLifeStyle.objects.all().filter(life_style=life_style)  # organ에 좋은 영양소 리스트
        # print(nutrient_list)
        # for num in range(good_nutrients_list.count()):
        #     try:
        #         supplement_obj = good_nutrients_list[num]
        #         print('옵젝', supplement_obj)
        #         serializer = SupplementSerializer(supplement_obj)
        #         return_list.append(serializer.data)
                        
        #     except IndexError:
        #         pass
        self.life_style = life_style
        print(life_style)
        if life_style == '올바른 영양 섭취가 중요한 어린이':
            self.search_prd_name('키즈')
            self.search_prd_name('우리아이')
            self.search_prd_name('아이사랑')
        elif life_style == '갱년기 증상으로 괴로운 50대 여성':
            self.search_pri_func('갱년기 여성')
            self.search_pri_func('갱년기여성')
        elif life_style == '남성호르몬 분비가 줄어드는 50대 갱년기 남성':
            self.search_pri_func('갱년기 남성')
            self.search_pri_func('전립선')
            self.search_pri_func('정자')
        elif life_style == '건강과 아름다움에 관심 많은 젊은 여성':
            self.search_prd_name('우먼')
            self.search_pri_func('월경')
            self.search_nutrition_facts('철')
        elif life_style == '공부에 시달리는 수험생':
            self.search_pri_func('기억력')
            self.search_nutrition_facts('은행잎 추출물')
        elif life_style == '에너지가 많이 필요한 10대 청소년(초등 후반〜중고생)':
            self.search_nutrition_facts('칼슘')
            self.search_nutrition_facts('철')
        elif life_style == '불규칙한 생활을 하는 젊은 남성':
            self.search_prd_name('미네랄')
            self.search_raw_material('미네랄')
        elif life_style == '노화가 진행되는 노년층':
            self.search_pri_func('인지력')
            self.search_nutrition_facts('은행잎 추출물')
        elif life_style == '키가 작아 고민인 청소년':
            self.search_nutrition_facts('칼슘')
            self.search_nutrition_facts('비타민 D')
        elif life_style == '영양보충에 특히 신경 써야하는 임산부':
            self.search_nutrition_facts('엽산')
        elif life_style == '운동을 많이 하는 사람':
            self.search_pri_func('근육,')
            self.search_pri_func('지구성')
        elif life_style == '과중한 업무에 시달리는 사람':
            self.search_nutrition_facts('EPA와 DHA의 합')
            self.search_pri_func('코엔자임Q10')
        elif life_style == '다이어트를 하는 사람':
            self.search_prd_name('다이어트')
        return Response(self.return_list)


#-------------------------함수형 view-----------------------------

# 아이디 중복 확인용
@api_view(['POST'])  # @api_view는 함수형 view를 사용할 때 사용
@permission_classes([permissions.AllowAny])
def is_id_duplicate(request):
    if request.method == 'POST':
        # 다수의 데이터 queryset 형태를 serialize화 하고자 할 때, many=True를 사용합니다.
        # 예시
        # data = [
        #    {'title': 'The bell jar', 'author': 'Sylvia Plath'},
        #    {'title': 'For whom the bell tolls', 'author': 'Ernest Hemingway'}
        # ]
        # serializer = BookSerializer(data=data, many=True)
        serializer = IsIdDuplicateSerializer(data=request.data)  # Request 객체인 request를 사용하여 request.data (POST, PUT, PATCH 사용 가능)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

        result = User.objects.filter(login_id=serializer.data['login_id'])
        result_cnt = result.count()

        if result_cnt == 0:
            return Response({"isValid": 1}, status=status.HTTP_200_OK)  # Response 객체를 사용하여 client에게 적절한 return type으로 제공
        else:
            return Response({ "isValid": 0}, status=status.HTTP_200_OK)


@api_view(['GET'])
def current_user(request):
    print('request.user', request.data)  # post하지 않았기 때문에 데이터가 비어 있게 출력된다.
    print(type(request.user), request.user)  # <class 'django.utils.functional.SimpleLazyObject'> changseon
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


# 아이디 찾기
@api_view(['POST'])
@permission_classes([permissions.AllowAny]) # 인증 필요없다
def find_id(request):
    result_cnt = 0
    if request.method == 'POST':

        serializer = FindIdSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

        result = User.objects.filter(email=serializer.data['email'])
        result_cnt = result.count()
        if result_cnt == 0:
            return Response({"message": "Invalid Email"}, status=status.HTTP_204_NO_CONTENT)

        response = {
            'login_id': result[0].login_id
        }
        return Response(response, status=status.HTTP_200_OK)
   

# signup
@api_view(['POST']) 
@permission_classes([permissions.AllowAny]) # 인증 필요없다
def signup(request):
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save() # DB 저장
        return Response(serializer.data, status=201) 

# login
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)
            
        if serializer.validated_data['login_id'] == "None": # login_id required
            return Response({'message': 'fail'}, status=status.HTTP_200_OK)
        # if serializer.validated_data['email'] == "None": # email required
        #     return Response({'message': 'fail'}, status=status.HTTP_200_OK)
        # if serializer.validated_data['nickname'] == "None": # nickname required
        #     return Response({'message': 'fail'}, status=status.HTTP_200_OK)
        result = User.objects.filter(login_id=serializer.data['login_id'])
        response = {
            'success': True,
            'token': serializer.data['token'], # 시리얼라이저에서 받은 토큰 전달
            'login_id': serializer.data['login_id'],
            'email': result[0].email,
            'nickname': result[0].nickname,
            'pk' : result[0].pk
        }
        return Response(response, status=status.HTTP_200_OK)


#--------------------------함수형 view--------------------------

#--------------------------긴 클래스 view--------------------------

class GoodForOrganToSupplements(APIView):
    permission_classes = [permissions.AllowAny]
    tmp_list = []  # serializer 하기 전에 data 있는지 없는지 확인하기 위한 용도
    return_list = []

    def search_pri_func(self, keyword):
        pri_func = Supplement.objects.all().filter(pri_func__icontains=keyword)
        for i in range(pri_func.count()):
            supplement_pk = pri_func[i]
            have = False

            # for item in self.tmp_list:   # 위에서 추가된 값들과 중복되는지 확인
            #     if supplement_pk == item:
            #         have = True

            if not have:
                serializer = SupplementSerializer(supplement_pk)
                self.return_list.append(serializer.data)
                self.tmp_list.append(supplement_pk)

    def get(self, request, organ, format=None):
        nutrient_list = GoodForOrgan.objects.all().filter(organ=organ)  # organ에 좋은 영양소 리스트
        self.tmp_list = []
        self.return_list = []
        # print(nutrient_list)
        # for num in range(nutrient_list.count()):
        #     try:
        #         nutrient_name = nutrient_list[num].nutrient
        #         nutrient_object = Nutrient.objects.all().filter(name=nutrient_name)  # 영양소 객체 구하기
        #         # print('영양소 이름: ', nutrient_name)
        #         # print('영양소 이름 갖는 영양소 객체: ', nutrient_object)

        #         nutrient_pk = nutrient_object[0].pk  # 영양소 pk 값 구하기 (정확히는 pk가 아니라 nutrient 객체 자체가 나옴)
        #         # print('nutrient_object: ', nutrient_object[0].pk)

        #         nutrition_facts_oject = NutritionFact.objects.all().filter(nutrient=nutrient_pk) # nutrient 가지고 있는 supplement 찾기
        #         for i in range(nutrition_facts_oject.count()):
        #             supplement_pk = nutrition_facts_oject[i].supplement
        #             serializer = SupplementSerializer(supplement_pk)
        #             self.return_list.append(serializer.data)
        #             self.tmp_list.append(supplement_pk)
                        
        #     except IndexError:
        #         pass

        # organ 활용하여 pri_func 속성에 좋다고 표시되어 있으면 찾기
        if organ == '요로':
            self.search_pri_func('요로')

        elif organ == '위':
            self.search_pri_func('위 건강')
            self.search_pri_func('담즙')

        elif organ == '간':
            self.search_pri_func('간 건강')
            self.search_pri_func('간건강')

        elif organ == '기관지':
            self.search_pri_func('재채기')
            self.search_pri_func('구강')

        elif organ == '기억력':  
            self.search_pri_func('기억력')

        elif organ == '긴장완화':  
            self.search_pri_func('긴장완화')

        elif organ == '수면':  
            self.search_pri_func('수면')

        elif organ == '인지기능':  
            self.search_pri_func('인지')

        elif organ == '피로':  
            self.search_pri_func('피로')

        elif organ == '눈':  
            self.search_pri_func('눈')

        elif organ == '피부':  
            self.search_pri_func('피부')

        elif organ == '장':  
            self.search_pri_func('배변활동')

        elif organ == '체지방':  
            self.search_pri_func('체지방')
        
        elif organ == '치아':  
            self.search_pri_func('치아')

        elif organ == '콜레스테롤':  
            self.search_pri_func('콜레스테롤')

        elif organ == '혈압':  
            self.search_pri_func('혈압')

        elif organ == '혈액':  
            self.search_pri_func('혈액')

        elif organ == '혈당':
            self.search_pri_func('혈당')

        elif organ == '갱년기건강':
            self.search_pri_func('갱년기')

        elif organ == '남성생식':
            self.search_pri_func('전립선')

        elif organ == '여성생식':
            self.search_pri_func('월경전')
        
        elif organ == '관절및뼈':
            self.search_pri_func('관절')
            self.search_pri_func('뼈')

        elif organ == '근육':
            self.search_pri_func('근육')

        elif organ == '면역':
            self.search_pri_func('면역')

        elif organ == '항산화':
           self.search_pri_func('항산화')

        elif organ == '정자운동성':
            self.search_pri_func('정자')

        # elif organ == '항산화':
            # pri_func = Supplement.objects.all().filter(pri_func__icontains='항산화')
            # for i in range(pri_func.count()):
            #     supplement_pk = pri_func[i]
            #     have = False

            #     for item in tmp_list:   # 위에서 추가된 값들과 중복되는지 확인
            #         if supplement_pk == item:
            #             have = True

            #     if not have:
            #         serializer = SupplementSerializer(supplement_pk)
            #         return_list.append(serializer.data)
            #         tmp_list.append(supplement_pk)

        return Response(self.return_list)
