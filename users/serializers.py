from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

# Получаем модель пользователя
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели пользователя.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        """
        Создание нового пользователя с хешированным паролем.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class GroupSerializer(serializers.ModelSerializer):
    """
    Сериализатор для групп.
    """
    class Meta:
        model = Group
        fields = ['id', 'name']
