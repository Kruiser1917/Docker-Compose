from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserViewSet

# Настройка маршрутов для ViewSet
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

# Маршруты приложения users
urlpatterns = [
    # JWT авторизация
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # CRUD для пользователей
    path('', include(router.urls)),
]
