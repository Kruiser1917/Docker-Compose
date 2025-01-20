from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from users.models import CustomUser
from users.serializers import UserSerializer


class UserCreateAPIView(CreateAPIView):
    """Создание польователя"""

    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    permission_class = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()
