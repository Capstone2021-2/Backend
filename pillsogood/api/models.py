from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class Nutrient(models.Model):
    type = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    upper = models.FloatField(blank=True, null=True)
    lower = models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=20)
    tmp_id = models.CharField(max_length=30)
    search_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class MainNutrient(models.Model):
    nutrient_pk = models.ForeignKey(Nutrient, on_delete=models.CASCADE, db_column='nutrient_pk')
    name = models.CharField(max_length=20)

    def __str__(self):
        return '{}'.format(self.name)

class Supplement(models.Model):
    type = models.IntegerField(default=1)
    name = models.CharField(max_length=100)
    image = models.ImageField(blank=True, null=True)
    company = models.CharField(max_length=50)
    exp_date = models.CharField(max_length=50)
    dispos = models.CharField(max_length=50)
    sug_use = models.CharField(max_length=100)
    warning = models.CharField(max_length=500)
    pri_func = models.CharField(max_length=500)
    raw_material = models.CharField(max_length=500)
    tmp_id = models.CharField(max_length=30)  # 01.json 파일에 적혀 있는 -id 값임
    search_count = models.IntegerField(default=0)  # 조회 수 
    
    # Review에 관련된 정보
    avg_rating = models.FloatField(default=0.0)
    review_num = models.IntegerField(default=0)
    taking_num = models.IntegerField(default=0)
    # 복용중인 사람 수
    
    nuntrient = models.ManyToManyField(
        Nutrient,
        through='NutritionFact'
    )

    def __str__(self):
        return self.name


class NutritionFact(models.Model):
    supplement = models.ForeignKey(Supplement, on_delete=models.CASCADE, db_column='supplement')
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE, db_column='nutrient')
    amount = models.FloatField()

    # 나중에 추가한 부분
    nutrient_name = models.CharField(max_length=100)
    upper = models.FloatField(blank=True, null=True)
    lower = models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return '{} : {}  {} '.format(self.supplement, self.nutrient, self.amount)

class Brand(models.Model):
    type = models.IntegerField(default=2)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, login_id, email, nickname, password=None):
        if not email:
            raise ValueError('must have user email')
        if not nickname:
            raise ValueError('must have user nickname')
        if not login_id:
            raise ValueError('must have user login_id')
        user = self.model(
            login_id = login_id,
            email=self.normalize_email(email),
            nickname = nickname
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login_id, email, nickname, password):
        user = self.create_user(
            login_id=login_id,
            email=self.normalize_email(email),
            nickname=nickname,
            password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):

    objects = UserManager()

    login_id = models.CharField(max_length=50,  unique=True)
    email = models.EmailField(max_length=100, default='', unique=True)
    nickname = models.CharField(max_length=20, default='', unique=True)
    gender = models.CharField(max_length=10)
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    age = models.ForeignKey('Age', blank=True, null= True, on_delete=models.CASCADE)
    body_type = models.ForeignKey('BodyType', blank=True, null=True, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'login_id'
    REQUIRED_FIELDS = ['email','nickname']

    def __str__(self):
        return self.login_id

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Review(models.Model):
    # user_nickname = models.CharField(max_length=30)
    # supplement = models.CharField(max_length=100)
    user_pk = models.ForeignKey(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    supplement = models.CharField(max_length=50)
    company = models.CharField(max_length=50)
    tmp_id = models.IntegerField()
    supplement_pk = models.ForeignKey(Supplement, on_delete=models.CASCADE)
    bodytype_pk = models.ForeignKey('BodyType', blank=True, null=True, on_delete=models.CASCADE)
    bodytype = models.CharField(max_length=10)
    age_pk = models.ForeignKey('Age', blank=True, null= True, on_delete=models.CASCADE)
    age = models.CharField(max_length=20)
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    rating = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(blank=True, null=True)
    text = models.CharField(max_length=1000)

    def __str__(self):
        return '{} : {} ({}) '.format(self.user_pk, self.supplement_pk, self.rating)

class TakingSupplements(models.Model):
    user_pk = models.ForeignKey(User, on_delete=models.CASCADE)
    supplement_pk  =models.ForeignKey(Supplement, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null= True)
    company = models.CharField(max_length=50, blank=True, null= True)
    tmp_id = models.CharField(max_length=30, blank=True, null= True)  # 01.json 파일에 적혀 있는 -id 값임

    def __str(self):
        return '{}이 복용 중인 영양제: {} '.format(self.user_pk, self.supplement_pk) 

class Age(models.Model):
    age_range = models.CharField(max_length=20)
    
    def __str__(self):
        return self.age_range

# 이번 model은 외래키를 사용하지 않고 만들어봄.
class AgeNutrient(models.Model):
    gender = models.CharField(max_length=10)
    ages = models.CharField(max_length=10)
    nutrient = models.CharField(max_length=30)
    upper = models.FloatField()
    lower = models.FloatField()

    def __str__(self):
        return '{} {} : {} '.format(self.gender, self.ages, self.nutrient)

class BodyType(models.Model):
    body_type = models.CharField(max_length=20)

    # Nutrient model(class)를 사용하여
    # 새로운 model 'GoodForBodyType' 생성
    # nutrient = models.ManyToManyField(
    #     'Nutrient',
    #     through = 'GoodForBodyType'
    # )

    def __str__(self):
        return self.body_type


class Organ(models.Model):
    organ = models.CharField(max_length=20, unique=True)
    # nutrient = models.ManyToManyField(
    #     'Nutrient',
    #     through = 'GoodForOrgan'
    # )

    def __str__(self):
        return self.organ

class LifeStyle(models.Model):
    life_style = models.CharField(max_length=50, unique=True)
    # nutrient = models.ManyToManyField(
    #     'Nutrient',
    #     through = 'GoodForLifeStyle'
    # )

    def __str__(self):
        return self.life_style


class GoodForBodyType(models.Model):
    bodytype =models.CharField(max_length=30)
    nutrient_pk = models.IntegerField()
    nutrient = models.CharField(max_length=50)

    def __str__(self):
        return '{} : {} '.format(self.bodytype, self.nutrient)


class GoodForOrgan(models.Model):
    organ = models.CharField(max_length=20)
    nutrient = models.CharField(max_length=50)

    def __str__(self):
        return '{} : {} '.format(self.organ, self.nutrient)


class GoodForLifeStyle(models.Model):
    life_style =models.CharField(max_length=50)
    nutrient = models.CharField(max_length=50)

    def __str__(self):
        return '{} : {} '.format(self.life_style, self.nutrient)


class GoodForAge(models.Model):
    age_range = models.CharField(max_length=30)
    gender = models.CharField(max_length=5)
    nutrient_pk = models.IntegerField()
    nutrient = models.CharField(max_length=50)

    def __str__(self):
        return '{} : {} '.format(self.age_range, self.nutrient)

class TopSearch(models.Model):
    nutrient_pk = models.IntegerField()
    nutrient = models.CharField(max_length=50)

    def __str__(self):
        return '{}'.format(self.nutrient)

class Caution(models.Model):
    name = models.CharField(max_length=50)
    caution = models.CharField(max_length=1000)

    def __str__(self):
        return '{}'.format(self.name)

class RequestSupplement(models.Model):

    supplement = models.CharField(max_length=100)
    company = models.CharField(max_length=50)
    image = models.ImageField(blank=True, null=True, upload_to="uploads")
