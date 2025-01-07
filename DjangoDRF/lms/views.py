from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.timezone import now
from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from .tasks import send_course_update_notification
from .services.stripe_service import create_checkout_session
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

class SubscriptionViewSet(ViewSet):
    """
    ViewSet для управления подписками.
    """
    def list(self, request):
        subscriptions = Subscription.objects.all()
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = SubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=True, methods=['get'])
    def lessons(self, request, pk=None):
        """Получить список уроков для курса."""
        course = self.get_object()
        lessons = Lesson.objects.filter(course=course)
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def update_course(self, request, pk=None):
        """Обновление курса и уведомление подписчиков."""
        course = self.get_object()
        serializer = self.get_serializer(course, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Уведомляем подписчиков через Celery
        send_course_update_notification.delay(course.id)
        return Response({'message': 'Course updated and notifications sent.'}, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        """Создание курса с асинхронным уведомлением."""
        course = serializer.save()
        send_course_update_notification.delay(course.id)

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        """Создание урока с уведомлением, если курс давно не обновлялся."""
        lesson = serializer.save()
        course = lesson.course
        if (now() - course.updated_at).total_seconds() > 4 * 3600:
            send_course_update_notification.delay(course.id)

    def perform_update(self, serializer):
        """Обновление урока с проверкой на время обновления курса."""
        lesson = serializer.save()
        course = lesson.course
        if (now() - course.updated_at).total_seconds() > 4 * 3600:
            send_course_update_notification.delay(course.id)

class CreatePaymentAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            session_url = create_checkout_session(request.data)
            return Response({'url': session_url}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    @action(detail=False, methods=['post'])
    def subscribe(self, request):
        """Подписка на курс."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response({'message': 'Subscription successful.'}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def user_subscriptions(self, request):
        """Получение списка подписок текущего пользователя."""
        subscriptions = Subscription.objects.filter(user=request.user)
        serializer = self.get_serializer(subscriptions, many=True)
        return Response(serializer.data)
