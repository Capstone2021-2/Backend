from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate
from . models import GoodForOrgan, NutritionFact, Supplement, User as UserTemp, Nutrient
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

class NutrientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutrient
        fields = ['pk', 'name', 'upper', 'lower', 'unit']


# image 추가해줘야함
class SupplementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplement
        fields = ['pk', 'name', 'company', 'exp_date', 'dispos', 'sug_use', 'warning', 'pri_func', 'raw_material', 'tmp_id']

class NutritionFactSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionFact
        fields = ['supplement', 'nutrient', 'amount']

class GoodForOrganSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodForOrgan
        fields = ['organ', 'nutrient']

#--------------------------------User ID 관련 Serializer---------------------------------------#

class IsIdDuplicateSerializer(serializers.Serializer):
    login_id = serializers.CharField(max_length=50)

    def validate(self, data):
        login_id = data.get("login_id", None)

        if login_id is None:
            return {'login_id' : 'None'}
        else:
            return { 'login_id' : login_id }
            

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTemp
        fields = ['login_id', 'email', 'nickname']


class FindIdSerializer(serializers.Serializer):
    # result = serializers.CharField(max_length=50)
    email = serializers.CharField(max_length=100)

    def validate(self, data):
        # print(data)
        email = data.get("email", None)

        # login_id = result
        if email is None:
            return { 'email ' : 'None' }
        else:
            return { 'email' :  email }


class UserCreateSerializer(serializers.Serializer):
    # 데이터 직렬화(Serializer)하기 위해 필요한 값들.
    # 사용자로 부터 validated_data를 받으면 그 값으로 채워 넣고
    # save() 해줌.
    login_id = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    nickname = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def create(self, validated_data):
        user = UserTemp.objects.create( # User 생성
            login_id=validated_data['login_id'],  # validated_data에서 받은 값으로 설정
            email=validated_data['email'],
            nickname=validated_data['nickname']
        )
        user.set_password(validated_data['password'])

        user.save()
        return user


JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class UserLoginSerializer(serializers.Serializer):
    login_id = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    # email = serializers.CharField(max_length=100)
    # nickname = serializers.CharField(max_length=20)


    def validate(self, data):
        login_id = data.get("login_id", None)
        password = data.get("password", None)
        # email = data.get("email", None)
        # nickname = data.get("nickname", None)
        # print(login_id)
        # print(password)
        user = authenticate(login_id=login_id, password=password)  # email, nickname
        # print('user info: ', user)
        if user is None:
            return {
                'login_id' : 'None'
            }
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload) # 토큰 발행
            update_last_login(None, user)
        except UserTemp.DoesNotExist:
            raise serializers.ValidationError(
                'User with given login_id and password does not exists'
            )
        return {
            'login_id': user.login_id,
            'token': jwt_token,
        }

#--------------------------------User ID 관련 Serializer---------------------------------------#

# class UserSerializerWithToken(serializers.ModelSerializer):
#     token = serializers.SerializerMethodField()
#     password = serializers.CharField(write_only=True)

#     def get_token(self, obj):
#         jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
#         jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

#         payload = jwt_payload_handler(obj)
#         token = jwt_encode_handler(payload)
#         return token

#     def create(self, validated_data):
#         password = validated_data.pop('password', None)
#         instance = self.Meta.model(**validated_data)
#         if password is not None:
#             instance.set_password(password)
#         instance.save()
#         return instance

#     class Meta:
#         model = User
#         fields = ('token', 'login_id', 'email', 'nickname', 'password')
