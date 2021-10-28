from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class Nutrient(models.Model):
    name = models.CharField(max_length=100)
    upper = models.FloatField(blank=True, null=True)
    lower = models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=20)
    tmp_id = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class MainNutrient(models.Model):
    name = models.ForeignKey(Nutrient, on_delete=models.CASCADE, db_column='name')

    def __str__(self):
        return '{}'.format(self.name)


class Supplement(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(blank=True, null=True)
    company = models.CharField(max_length=50)
    exp_date = models.CharField(max_length=50)
    dispos = models.CharField(max_length=50)
    sug_use = models.CharField(max_length=100)
    warning = models.CharField(max_length=500)
    pri_func = models.CharField(max_length=500)
    raw_material = models.CharField(max_length=500)
    tmp_id = models.CharField(max_length=30)
    nuntrient = models.ManyToManyField(
        Nutrient,
        through='NutritionFact'
    )
    user_review = models.ManyToManyField(
        'User',
        through='Review'
    )

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.pk == other.pk
        


class NutritionFact(models.Model):
    supplement = models.ForeignKey(Supplement, on_delete=models.CASCADE, db_column='supplement')
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE, db_column='nutrient')
    amount = models.FloatField()

    def __str__(self):
        return '{} : {}  {} '.format(self.supplement, self.nutrient, self.amount)


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


class Review(models.Model):

    # RATING_CHOICES = (
    #     ('ONE', 1)
    #     ('TWO', 2)
    #     ('THREE', 3)
    #     ('FOUR', 4)
    #     ('FIVE', 5)
    # )
    user_nicname = models.ForeignKey(User, on_delete=models.CASCADE)
    supplement = models.ForeignKey(Supplement, on_delete=models.CASCADE)
    # rating = models.IntegerField(max_length=2, choices=RATING_CHOICES)
    rating = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)
    image = models.ImageField()
    text = models.CharField(max_length=1000)

    def __str__(self):
        return '{} : {} ({}) '.format(self.user_nicname, self.supplement, self.rating)




class GoodForBodyType(models.Model):
    # body_type = models.ForeignKey(BodyType, on_delete=models.CASCADE)
    # nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)
    body_type =models.CharField(max_length=30)
    nutrient = models.CharField(max_length=50)

    def __str__(self):
        return '{} : {} '.format(self.body_type, self.nutrient)


class GoodForOrgan(models.Model):
    organ = models.CharField(max_length=20)
    nutrient = models.CharField(max_length=50)

    def __str__(self):
        return '{} : {} '.format(self.organ, self.nutrient)


class GoodForLifeStyle(models.Model):
    # life_style = models.ForeignKey(LifeStyle, on_delete=models.CASCADE)
    # nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)

    life_style =models.CharField(max_length=50)
    nutrient = models.CharField(max_length=50)

    def __str__(self):
        return '{} : {} '.format(self.life_style, self.nutrient)
