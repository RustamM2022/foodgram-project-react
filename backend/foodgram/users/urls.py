from django.urls import include, path, re_path
from rest_framework import routers

from . import views
from .views import CustomUserViewSet

app_name = 'users'

router = routers.DefaultRouter()


router.register(r'users', CustomUserViewSet, basename='users')
router.register(r'users', views.SubscriptionViewSet, basename='subscribe')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken'))
]
