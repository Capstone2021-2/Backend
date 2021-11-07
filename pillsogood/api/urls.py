from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

router =  routers.DefaultRouter()
router.register(r'main_nutrients', views.MainNutrientViewSet, basename='main_nutrients')  # nutrient_pk 값, nutrient_name 제공
router.register(r'nutrients', views.NutrientViewSet, basename='nutrients')  # 영양소
router.register(r'supplements', views.SupplementViewSet, basename='supplements')  # 영양제
router.register(r'nutrition_facts', views.NutritionFactViewSet, basename='nutrition_facts')  # 영양제가 함유하고 있는 영양소
router.register(r'organs', views.OrganViewSet, basename='organs')  # 몸 기능
router.register(r'good_for_organs', views.GoodForOrganViewSet, basename='good_for_organs')  # 몸 기능에 좋은 영양소
router.register(r'brands', views.BrandViewSet, basename='brands')  # 약 회사
router.register(r'reviews', views.ReviewViewSet, basename='reviews')  # 리뷰
router.register(r'ages', views.AgeViewSet, basename='ages')  # 나이
router.register(r'body_types', views.BodyTypeViewSet, basename='body_types')  # 체질
router.register(r'life_styles', views.LifeStyleViewSet, basename='life_styles')  # 라이프 스타일
router.register(r'good_for_life_styles', views.GoodForLifeStyleViewSet, basename='good_for_lifestyles')  # 라이프 스타일에 맞는 영양소
# router.register(r'age_nutrients', views.SupplementViewSet)


urlpatterns = [
    path('', include(router.urls)),  # include는 폴더 자체를 저장하는 것임.
    path('nutrients/name/<str:name>', views.NutrientDetail.as_view()),  # 영양소 검색
    path('nutrition_facts/<int:nutrient>', views.NutritionFactDetail.as_view()),  # 영양소 pk 값으로 어떤 영양제가 이 영양소 갖고 있는지
    path('good_for_organs/<str:organ>', views.GoodForOrganDetail.as_view()),
    path('good_for_organs_supplements/<str:organ>', views.GoodForOrganToSupplements.as_view()), # organ에 좋은 영양제 검색
    path('brands/name/<str:brand>', views.BrandToSupplements.as_view()),  # brand로 영양제 검색
    path('good_for_life_styles/<str:life_style>', views.GoodForLifeStyleDetail.as_view()),
    path('good_for_life_styles_supplements/<str:life_style>', views.LifeStyleToSupplements.as_view()),  # life_style로 영양제 검색
    path('reviews/user/<str:user_pk>', views.ReviewUser.as_view()),  # user가 작성한 리뷰 모아볼 때
    path('reviews/supplements/<str:supplement_pk>', views.ReviewSupplement.as_view()),  # supplement별로 리뷰 볼 때
    path('tmp_best_supplements/<str:name>', views.TmpBestSupplements.as_view()), 
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