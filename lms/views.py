from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner


class CourseViewSet(ModelViewSet):
    """
    ViewSet для работы с курсами.
    - Модераторы могут просматривать и редактировать курсы.
    - Владельцы могут создавать, редактировать и удалять только свои курсы.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        """
        Возвращает только те курсы, которые принадлежат авторизованному пользователю,
        если он не модератор.
        """
        if self.request.user.groups.filter(name='Moderators').exists():
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)

    def get_permissions(self):
        """
        Настройка прав доступа:
        - create: только для авторизованных пользователей.
        - retrieve, update, partial_update: доступ для владельцев и модераторов.
        - destroy: только для владельцев.
        """
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsOwner]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        """
        Привязывает создаваемый курс к авторизованному пользователю.
        """
        serializer.save(owner=self.request.user)


class LessonViewSet(ModelViewSet):
    """
    ViewSet для работы с уроками.
    - Модераторы могут просматривать и редактировать уроки.
    - Владельцы могут создавать, редактировать и удалять только свои уроки.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_queryset(self):
        """
        Возвращает только те уроки, которые принадлежат авторизованному пользователю,
        если он не модератор.
        """
        if self.request.user.groups.filter(name='Moderators').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)

    def get_permissions(self):
        """
        Настройка прав доступа:
        - create: только для авторизованных пользователей.
        - retrieve, update, partial_update: доступ для владельцев и модераторов.
        - destroy: только для владельцев.
        """
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsOwner]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        """
        Привязывает создаваемый урок к авторизованному пользователю.
        """
        serializer.save(owner=self.request.user)
