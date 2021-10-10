from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.

class Nutrient(models.Model):
    name = models.CharField(max_length=50)
    upper = models.FloatField()
    lower = models.FloatField()
    unit = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Supplement(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField()
    company = models.CharField(max_length=50)
    exp_date = models.CharField(max_length=50)
    dispos = models.CharField(max_length=50)
    sug_use = models.CharField(max_length=100)
    warning = models.CharField(max_length=500)
    pri_func = models.CharField(max_length=500)
    raw_material = models.CharField(max_length=500)
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


class NutritionFact(models.Model):
    supplement = models.ForeignKey(Supplement, on_delete=models.CASCADE)
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)
    amount = models.FloatField()

    def __str__(self):
        return '{} : {} ({})'.format(self.supplement, self.nutrient, self.amount)


class User(models.Model):
    user_id = models.CharField(max_length=50)
    age = models.ForeignKey('Age', null=False, on_delete=models.CASCADE)
    height = models.FloatField()
    weight = models.FloatField()
    body_type = models.ForeignKey('BodyType', null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.login_id

class Age(models.Model):
    age_range = models.CharField(max_length=20)

    def __str__(self):
        return self.age_range


class BodyType(models.Model):
    body_type = models.CharField(max_length=20)

    # Nutrient model(class)를 사용하여
    # 새로운 model 'GoodForBodyType' 생성
    nutrient = models.ManyToManyField(
        'Nutrient',
        through = 'GoodForBodyType'
    )

    def __str__(self):
        return self.body_type


class Organ(models.Model):
    organ = models.CharField(max_length=20)
    nutrient = models.ManyToManyField(
        'Nutrient',
        through = 'GoodForOrgan'
    )

    def __str__(self):
        return self.organ

class LifeStyle(models.Model):
    life_style = models.CharField(max_length=50)
    nutrient = models.ManyToManyField(
        'Nutrient',
        through = 'GoodForLifeStyle'
    )

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
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    supplement = models.ForeignKey(Supplement, on_delete=models.CASCADE)
    # rating = models.IntegerField(max_length=2, choices=RATING_CHOICES)
    rating = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)
    image = models.ImageField()
    text = models.CharField(max_length=1000)

    def __str__(self):
        return '{} : {} ({}) '.format(self.user_id, self.supplement, self.rating)




class GoodForBodyType(models.Model):
    body_type = models.ForeignKey(BodyType, on_delete=models.CASCADE)
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)

    def __str__(self):
        return '{} : {} '.format(self.body_type, self.nutrient)


class GoodForOrgan(models.Model):
    organ = models.ForeignKey(Organ, on_delete=models.CASCADE)
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)

    def __str__(self):
        return '{} : {} '.format(self.organ, self.nutrient)


class GoodForLifeStyle(models.Model):
    life_style = models.ForeignKey(LifeStyle, on_delete=models.CASCADE)
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)

    def __str__(self):
        return '{} : {} '.format(self.life_style, self.nutrient)