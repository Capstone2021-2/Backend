from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

router =  routers.DefaultRouter()
router.register(r'nutrient', views.NutrientViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('user/jwt-auth/', obtain_jwt_token),
    path('user/jwt-auth/verify/', verify_jwt_token),
    path('user/jwt-auth/refresh/', refresh_jwt_token),
    path('user/signup', views.signup),
    path('user/login', views.login),
    path('user/current/', views.current_user),

    # path('user/', views.UserList),
    #path('user')
    # path('api-auth', include('rest_framework.urls')),
]