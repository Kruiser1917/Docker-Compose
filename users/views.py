from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

# Получаем модель пользователя
User = get_user_model()


class UserViewSet(ModelViewSet):
    """
    ViewSet для CRUD операций над пользователями.
    - Регистрация пользователей доступна всем.
    - Все остальные действия требуют авторизации.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Определение прав доступа на основе действий.
        - Регистрация (create) доступна всем (AllowAny).
        - Остальные действия требуют авторизации (IsAuthenticated).
        """
        if self.action in ['create']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]
