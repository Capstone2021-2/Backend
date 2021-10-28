from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

router =  routers.DefaultRouter()
router.register(r'main_nutrients', views.MainNutrientViewSet, basename='main_nutrients')  # nutrient_pk 값, nutrient_name 제공
router.register(r'nutrients', views.NutrientViewSet, basename='nutrients')
router.register(r'supplements', views.SupplementViewSet, basename='supplements')
router.register(r'nutrition_facts', views.NutritionFactViewSet, basename='nutrition_facts')
router.register(r'organs', views.OrganViewSet, basename='organs')
router.register(r'good_for_organs', views.GoodForOrganViewSet, basename='good_for_organs')
router.register(r'brands', views.BrandViewSet, basename='brands')
# router.register(r'age_nutrients', views.SupplementViewSet)


urlpatterns = [
    path('', include(router.urls)),  # include는 폴더 자체를 저장하는 것임.
    path('nutrients/name/<str:name>', views.NutrientDetail.as_view()),
    path('nutrition_facts/<int:nutrient>', views.NutritionFactDetail.as_view()),
    path('good_for_organs/<str:organ>', views.GoodForOrganDetail.as_view()),
    path('good_for_organs_supplements/<str:organ>', views.GoodForOrganToSupplements.as_view()), # organ에 좋은 영양제 검색
    path('brands/name/<str:brand>', views.BrandToSupplements.as_view()),  # brand로 영양제 검색
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