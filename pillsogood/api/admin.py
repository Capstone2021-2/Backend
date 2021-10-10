from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Nutrient)
admin.site.register(Supplement)
admin.site.register(NutritionFact)
admin.site.register(User)
admin.site.register(Age)
admin.site.register(BodyType)
admin.site.register(Organ)
admin.site.register(LifeStyle)
admin.site.register(Review)
admin.site.register(GoodForBodyType)
admin.site.register(GoodForOrgan)
admin.site.register(GoodForLifeStyle)
