# from django.shortcuts import render

from .models import *
from rest_framework import viewsets
from .serializer import *

from django.http import HttpResponseRedirect
from rest_framework import permissions, status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
import django_filters.rest_framework

#--------------------------클래스형 view--------------------------

class NutrientViewSet(viewsets.ModelViewSet):
    queryset = Nutrient.objects.all()
    serializer_class = NutrientSerializer
    permission_classes = [permissions.AllowAny]
    # permission_classes = [permissions.IsAuthenticated]


class SupplementViewSet(viewsets.ModelViewSet):
    queryset = Supplement.objects.all().order_by('name')
    serializer_class = SupplementSerializer
    permission_classes = [permissions.AllowAny]


class NutritionFactViewSet(viewsets.ModelViewSet):
    queryset = Supplement.objects.all()
    serializer_class = SupplementSerializer
    permission_classes = [permissions.AllowAny]


class AgeNutrientViewSet(viewsets.ModelViewSet):
    queryset = Supplement.objects.all()
    serializer_class = SupplementSerializer
    permission_classes = [permissions.AllowAny]


#-------------------------함수형 view-----------------------------

# 아이디 중복 확인용
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def is_id_duplicate(request):
    if request.method == 'POST':
        serializer = IsIdDuplicateSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

        result = User.objects.filter(login_id=serializer.data['login_id'])
        result_cnt = result.count()

        if result_cnt == 0:
            return Response({"isValid": 1}, status=status.HTTP_200_OK)
        else:
            return Response({ "isValid": 0}, status=status.HTTP_200_OK)



@api_view(['GET'])
def current_user(request):
    print('request.user', request.data)
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