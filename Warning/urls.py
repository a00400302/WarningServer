from django.urls import path, re_path, include
from . import views
from rest_framework.authtoken import views as v
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'pushuser', views.PushViewSet)
router.register(r'warning', views.WaringViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    re_path('', include(router.urls)),
    re_path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path('api_token_auth/',v.obtain_auth_token),
    re_path('changepwd/',views.changepwd),
    re_path('pushsave/',views.pushsave),
]
