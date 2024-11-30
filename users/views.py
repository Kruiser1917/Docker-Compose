from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework import status
from .serializers import UserSerializer

User = get_user_model()


class RegisterView(APIView):
    """
    API для регистрации пользователей.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Обработка регистрации нового пользователя.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Пользователь успешно зарегистрирован."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    """
    API для получения информации о текущем пользователе.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Возвращает данные текущего пользователя.
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
