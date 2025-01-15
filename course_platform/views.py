import datetime
from django.utils import timezone
from rest_framework import viewsets, generics, views
from rest_framework.permissions import IsAuthenticated
from course_platform.models import Course, Lesson, Subscription
from course_platform.paginators import CoursePaginator, LessonPaginator
from course_platform.serializers import CourseSerializers, LessonSerializers, CourseDetailSerializers
from users.permissions import IsModer, IsOwner
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from course_platform.task import send_course_update_notification


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(operation_description="description from swagger_auto_schema via method_decorator"),
)
class CourseViewSet(viewsets.ModelViewSet):
    """Course endpoint"""
    pagination_class = CoursePaginator
    queryset = Course.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializers
        return CourseSerializers

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModer | IsOwner,)
        return super().get_permissions()

    def perform_update(self, serializer):
        course = serializer.save()
        now = timezone.now()

        # Проверяем время последнего обновления
        if course.updated_at < now - datetime.timedelta(hours=4):
            send_course_update_notification.delay(course.id)


class LessonCreateAPIView(generics.CreateAPIView):
    """Lesson creation enpoint."""
    serializer_class = LessonSerializers
    permission_classes = (~IsModer, IsAuthenticated)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """Enpoint view lessons."""
    pagination_class = LessonPaginator
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Enpoint viewing lesson."""
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Lesson update endpoint."""
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Endpoint for deleting a lesson."""
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsOwner | ~IsModer)


class SubscriptionView(views.APIView):
    """Subscription endpoint."""
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        course_id = request.data.get('course_id')
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=request.user, course=course_item)

        if subs_item.exists():

            subs_item.delete()
            message = 'Подписка удалена'
        else:

            Subscription.objects.create(user=request.user, course=course_item)
            message = 'Подписка добавлена'

        return Response({"message": message}, status=status.HTTP_200_OK)

