from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import validate_video_url


class LessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Lesson.
    """
    video_url = serializers.URLField(
        required=False,
        allow_null=True,
        validators=[validate_video_url]
    )

    class Meta:
        model = Lesson
        fields = ["id", "title", "description", "video_url", "course"]
        read_only_fields = ["id"]


class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Course.
    """
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ["id", "title", "description", "owner", "lessons", "is_subscribed"]
        read_only_fields = ["id", "lessons", "is_subscribed"]

    def get_is_subscribed(self, obj):
        """
        Проверяет, подписан ли текущий пользователь на курс.
        """
        user = self.context.get("request").user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Subscription.
    """
    class Meta:
        model = Subscription
        fields = ["id", "user", "course"]
        read_only_fields = ["id", "user"]

    def validate_course(self, value):
        """
        Проверка на дублирование подписки.
        """
        user = self.context["request"].user
        if Subscription.objects.filter(user=user, course=value).exists():
            raise serializers.ValidationError("Вы уже подписаны на этот курс.")
        return value
