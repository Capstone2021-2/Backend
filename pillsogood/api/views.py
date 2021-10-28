# from django.shortcuts import render

from django.utils.regex_helper import contains
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

    def get_object(self, name):
        print("이름 출력:", name)
        try:
            return Nutrient.objects.get(name=name)
        except Nutrient.DoesNotExist:
            raise Http404
    def get(self, request, name, format=None):
        nutrient = self.get_object(name)
        serializer = NutrientSerializer(nutrient)
        return Response(serializer.data)
        



class SupplementViewSet(viewsets.ModelViewSet):
    queryset = Supplement.objects.all().order_by('name')
    serializer_class = SupplementSerializer
    permission_classes = [permissions.AllowAny]


class SupplementDetail(APIView):
    permission_classes = [permissions.AllowAny]

    def get_object(self, name):
        print("이름 출력:", name)
        try:
            return Supplement.objects.get(name=name)
        except Supplement.DoesNotExist:
            raise Http404
    def get(self, request, name, format=None):
        supplement = self.get_object(name)
        serializer = SupplementSerializer(supplement)
        return Response(serializer.data)



class NutritionFactViewSet(viewsets.ModelViewSet):
    queryset = NutritionFact.objects.all()
    serializer_class = NutritionFactSerializer
    permission_classes = [permissions.AllowAny]


class NutritionFactDetail(APIView):
    permission_classes = [permissions.AllowAny]

    def get_object(self, nutrient):
        print("이름 출력:", nutrient)
        try:
            return NutritionFact.objects.all().filter(nutrient=nutrient)  # 여러 데이터 전달하기 위해
        except NutritionFact.DoesNotExist:
            raise Http404
    def get(self, request, nutrient, format=None):
        nutrition = self.get_object(nutrient)
        serializer = NutritionFactSerializer(nutrition, many=True)  # 결과가 여러개 나오기 때문에 many = True
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


class GoodForOrganToSupplements(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, organ, format=None):
        nutrient_list = GoodForOrgan.objects.all().filter(organ=organ)  # organ에 좋은 영양소 리스트
        tmp_list = []  # serializer 하기 전에 data 있는지 없는지 확인하기 위한 용도
        return_list = []
        # print(nutrient_list)
        for num in range(nutrient_list.count()):
            try:
                nutrient_name = nutrient_list[num].nutrient
                nutrient_object = Nutrient.objects.all().filter(name=nutrient_name)  # 영양소 객체 구하기
                # print('영양소 이름: ', nutrient_name)
                # print('영양소 이름 갖는 영양소 객체: ', nutrient_object)

                nutrient_pk = nutrient_object[0].pk  # 영양소 pk 값 구하기 (정확히는 pk가 아니라 nutrient 객체 자체가 나옴)
                # print('nutrient_object: ', nutrient_object[0].pk)

                nutrition_facts_oject = NutritionFact.objects.all().filter(nutrient=nutrient_pk) # nutrient 가지고 있는 supplement 찾기
                for i in range(nutrition_facts_oject.count()):
                    supplement_pk = nutrition_facts_oject[i].supplement
                    serializer = SupplementSerializer(supplement_pk)
                    return_list.append(serializer.data)
                    tmp_list.append(supplement_pk)
                        
            except IndexError:
                pass

        # organ 활용하여 pri_func 속성에 좋다고 표시되어 있으면 찾기
        if organ == '요로':
            pri_func = Supplement.objects.all().filter(pri_func__icontains=organ)
            for i in range(pri_func.count()):
                supplement_pk = pri_func[i]
                have = False

                for item in tmp_list:   # 위에서 추가된 값들과 중복되는지 확인
                    if supplement_pk == item:
                        have = True

                if not have:
                    serializer = SupplementSerializer(supplement_pk)
                    return_list.append(serializer.data)
                    tmp_list.append(supplement_pk)
        return Response(return_list)
            

class AgeNutrientViewSet(viewsets.ModelViewSet):
    queryset = AgeNutrient.objects.all()
    serializer_class = SupplementSerializer
    permission_classes = [permissions.AllowAny]


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
        }
        return Response(response, status=status.HTTP_200_OK)