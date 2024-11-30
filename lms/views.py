from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с курсами.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        """
        Переопределяем метод для добавления контекста запроса.
        """
        user = self.request.user
        if user.is_authenticated:
            return Course.objects.all()
        return Course.objects.none()


class LessonViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с уроками.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_queryset(self):
        """
        Переопределяем метод для фильтрации уроков по курсам.
        """
        course_id = self.request.query_params.get('course_id')
        if course_id:
            return Lesson.objects.filter(course_id=course_id)
        return super().get_queryset()


class SubscriptionAPIView(APIView):
    """
    APIView для работы с подписками на курсы.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Метод для добавления или удаления подписки.
        """
        user = request.user
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)

        # Проверяем, есть ли подписка
        subscription, created = Subscription.objects.get_or_create(user=user, course=course)
        if created:
            return Response({'message': 'Подписка добавлена'}, status=status.HTTP_201_CREATED)
        else:
            subscription.delete()
            return Response({'message': 'Подписка удалена'}, status=status.HTTP_200_OK)
