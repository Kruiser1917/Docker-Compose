from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonViewSet, SubscriptionViewSet, CreatePaymentAPIView

# Создаем роутер
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'lessons', LessonViewSet, basename='lessons')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscriptions')

urlpatterns = [
    path('', include(router.urls)),  # Подключаем маршруты роутера
    path('create-payment/', CreatePaymentAPIView.as_view(), name='create-payment'),
]
