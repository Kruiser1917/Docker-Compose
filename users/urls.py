from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.permissions import AllowAny
from users.apps import UsersConfig
from users.views import UserProfileViewSet, PaymentsViewSet, CustomsUserViewSet, CustomUserCreateAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = UsersConfig.name


router = DefaultRouter()
router.register(r'profile', UserProfileViewSet, basename='userprofile')
router.register(r'payments', PaymentsViewSet, basename='payments')
router.register(r'users', CustomsUserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', CustomUserCreateAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
]
