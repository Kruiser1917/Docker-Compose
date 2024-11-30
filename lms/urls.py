from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonViewSet, SubscriptionAPIView

router = DefaultRouter()
router.register('courses', CourseViewSet, basename='courses')
router.register('lessons', LessonViewSet, basename='lessons')

urlpatterns = [
    path('', include(router.urls)),
    path('subscriptions/', SubscriptionAPIView.as_view(), name='subscriptions'),
]
