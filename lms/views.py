from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course, Payment
from .models import Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer
from .services.stripe_service import create_product, create_price, create_checkout_session


def post(request):
    course_id = request.data.get("course_id")
    course = Course.objects.get(id=course_id)

    # Создаем продукт в Stripe
    stripe_product = create_product(name=course.title)

    # Создаем цену для продукта
    stripe_price = create_price(product_id=stripe_product["id"], amount=int(course.price * 100))

    # Создаем сессию для оплаты
    success_url = "https://example.com/success"
    cancel_url = "https://example.com/cancel"
    stripe_session = create_checkout_session(price_id=stripe_price["id"], success_url=success_url,
                                             cancel_url=cancel_url)

    # Сохраняем данные о платеже
    Payment.objects.create(
        course=course,
        stripe_product_id=stripe_product["id"],
        stripe_price_id=stripe_price["id"],
        stripe_session_id=stripe_session["id"],
    )

    return Response({"url": stripe_session["url"]}, status=status.HTTP_201_CREATED)


class CreatePaymentAPIView(APIView):
    pass


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


def post(request):
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


class SubscriptionAPIView(APIView):
    """
    APIView для работы с подписками на курсы.
    """
    permission_classes = [IsAuthenticated]
