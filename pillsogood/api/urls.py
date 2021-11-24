from django.urls import path, include
from django.conf.urls import url

from . import views
from rest_framework import routers
from rest_framework import permissions
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


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
router.register(r'taking_supplements', views.TakingSupplementsViewSet, basename='taking_supplements')  # 복용 중인 영양제
#router.register(r'search', views.SearchSet, basename='search')  # 영양소, 영양제, 브랜드 검색 기능
#router.register(r'user_edit', views.UserEdit, basename='user_edit')  # 유저 변경
# router.register(r'age_nutrients', views.SupplementViewSet)

# swagger를 위한 것
schema_url_patterns = [ 
    # path('', include(router.urls)),  # include는 폴더 자체를 저장하는 것임.
    path('nutrients/name/<str:nutrient>', views.NutrientDetail.as_view()),  # (영양소 pk가 아니라) 영양소 이름으로 영양소검색

    # 함유 영양소
    path('nutrition_facts/nutrient_to_supplement/<int:nutrient_pk>', views.NutritionFactNutrientToSupplement.as_view()),  # 영양소 pk 값으로 어떤 영양제가 이 영양소 갖고 있는지
    path('nutrition_facts/supplement_to_nutrient/<int:supplement_pk>', views.NutritionFactSupplementToNutrient.as_view()),  # 영양제 pk 값으로 어떤 영양소들을 가지고 있는 지

    # 기능들
    path('good_for_organs/<str:organ>', views.GoodForOrganDetail.as_view()),
    path('good_for_organs_supplements/<str:organ>', views.GoodForOrganToSupplements.as_view()), # organ에 좋은 영양제 검색

    # 브랜드
    path('brands/name/<str:brand>', views.BrandToSupplements.as_view()),  # brand로 영양제 검색

    # 라이프 스타일 관련
    path('good_for_life_styles/<str:life_style>', views.GoodForLifeStyleDetail.as_view()),
    path('good_for_life_styles_supplements/<str:life_style>', views.LifeStyleToSupplements.as_view()),  # life_style로 영양제 검색

    # 리뷰 관리
    path('reviews/user/<int:user_pk>', views.ReviewUser.as_view()),  # user별 리뷰 볼 때
    path('reviews/supplements/<int:supplement_pk>', views.ReviewSupplement.as_view()),  # supplement별로 리뷰 볼 때
    path('reviews/delete/<int:user_pk>/<int:supplement_pk>', views.ReviewUser.as_view()),  # user_pk와 supplement로 삭제할 때

    # 복용중인 영양제
    path('taking_supplements/user/<int:user_pk>', views.TakingSupplementsUser.as_view()),  # user별 복용하고 있는 영양제 볼 때
    path('taking_supplements/delete/<int:user_pk>/<int:supplement_pk>', views.TakingSupplementsDelete.as_view()),  # user가 삭제할 때

    # 검색
    path('search/<str:search_name>', views.SearchSet.as_view()),  # search_name으로 해당 영양소, 영양제, 브랜드 검색

    path('tmp_best_supplements/<str:name>', views.TmpBestSupplements.as_view()), 
    path('user/jwt-auth/', obtain_jwt_token),
    path('user/jwt-auth/verify/', verify_jwt_token),
    path('user/jwt-auth/refresh/', refresh_jwt_token),

    # user 회원가입 로그인 관련
    path('user/signup', views.signup),
    path('user/login', views.login),
    path('user/find-id/', views.find_id),
    path('user/duplicate-id', views.is_id_duplicate),

    ]


schema_view = get_schema_view(
    openapi.Info(
        title="Open API",
        default_version='v1',
        description="시스템 API",
        terms_of_service="https://www.google.com/policies/terms/",
        ),
        public=True, 
        permission_classes=(permissions.AllowAny,), 
        patterns=schema_url_patterns, 
    )


urlpatterns = [
    path('', include(router.urls)),  # include는 폴더 자체를 저장하는 것임.
    path('nutrients/name/<str:nutrient>', views.NutrientDetail.as_view()),  # (영양소 pk가 아니라) 영양소 이름으로 영양소검색

    # 함유 영양소
    path('nutrition_facts/nutrient_to_supplement/<int:nutrient_pk>', views.NutritionFactNutrientToSupplement.as_view()),  # 영양소 pk 값으로 어떤 영양제가 이 영양소 갖고 있는지
    path('nutrition_facts/supplement_to_nutrient/<int:supplement_pk>', views.NutritionFactSupplementToNutrient.as_view()),  # 영양제 pk 값으로 어떤 영양소들을 가지고 있는 지

    # 기능들
    path('good_for_organs/<str:organ>', views.GoodForOrganDetail.as_view()),
    path('good_for_organs_supplements/<str:organ>', views.GoodForOrganToSupplements.as_view()), # organ에 좋은 영양제 검색

    # 브랜드
    path('brands/name/<str:brand>', views.BrandToSupplements.as_view()),  # brand로 영양제 검색

    # 라이프 스타일 관련
    path('good_for_life_styles/<str:life_style>', views.GoodForLifeStyleDetail.as_view()),
    path('good_for_life_styles_supplements/<str:life_style>', views.LifeStyleToSupplements.as_view()),  # life_style로 영양제 검색

    # 리뷰 관리
    path('reviews/user/<int:user_pk>', views.ReviewUser.as_view()),  # user별 리뷰 볼 때
    path('reviews/supplements/<int:supplement_pk>', views.ReviewSupplement.as_view()),  # supplement별로 리뷰 볼 때
    path('reviews/delete/<int:user_pk>/<int:supplement_pk>', views.ReviewUser.as_view()),  # user_pk와 supplement로 삭제할 때

    # 복용중인 영양제
    path('taking_supplements/user/<int:user_pk>', views.TakingSupplementsUser.as_view()),  # user별 복용하고 있는 영양제 볼 때
    path('taking_supplements/delete/<int:user_pk>/<int:supplement_pk>', views.TakingSupplementsDelete.as_view()),  # user가 삭제할 때

    # 검색
    path('search/<str:search_name>', views.SearchSet.as_view()),  # search_name으로 해당 영양소, 영양제, 브랜드 검색

    path('tmp_best_supplements/<str:name>', views.TmpBestSupplements.as_view()), 
    path('user/jwt-auth/', obtain_jwt_token),
    path('user/jwt-auth/verify/', verify_jwt_token),
    path('user/jwt-auth/refresh/', refresh_jwt_token),

    # user 회원가입 로그인 관련
    path('user/signup', views.signup),
    path('user/login', views.login),
    path('user/find-id/', views.find_id),
    path('user/duplicate-id', views.is_id_duplicate),
    path('user/edit', views.edit_user),

    # path('user/current/', views.current_user),
    path('user/dj-rest-auth/', include('dj_rest_auth.urls')),
    path('', include('django.contrib.auth.urls')),

    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


]