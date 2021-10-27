from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

router =  routers.DefaultRouter()
router.register(r'nutrients', views.NutrientViewSet, basename='nutrients')
router.register(r'supplements', views.SupplementViewSet, basename='supplements')
# router.register(r'nutrition_facts', views.NutrientViewSet)
# router.register(r'age_nutrients', views.SupplementViewSet)

urlpatterns = [
    path('', include(router.urls)),  # include는 폴더 자체를 저장하는 것임.
    path('supplements/<str:name>', views.SupplementDetail.as_view()),
    path('user/jwt-auth/', obtain_jwt_token),
    path('user/jwt-auth/verify/', verify_jwt_token),
    path('user/jwt-auth/refresh/', refresh_jwt_token),
    path('user/signup', views.signup),
    path('user/login', views.login),
    path('user/current/', views.current_user),
    path('user/dj-rest-auth/', include('dj_rest_auth.urls')),
    path('', include('django.contrib.auth.urls')),
    path('user/find-id/', views.find_id),
    path('user/duplicate-id', views.is_id_duplicate)
]