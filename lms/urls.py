from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CourseViewSet, LessonViewSet

# Роутеры для автоматической генерации маршрутов
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lessons', LessonViewSet, basename='lesson')

urlpatterns = [
    path('', include(router.urls)),  # Включаем маршруты роутера
]
