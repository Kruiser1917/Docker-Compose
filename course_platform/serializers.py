from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from course_platform.models import Course, Lesson, Subscription
from course_platform.validators import LinkToVideoValidator


class CourseSerializers(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False


class LessonSerializers(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
        validators=[LinkToVideoValidator(field='link_to_video')]


class CourseDetailSerializers(serializers.ModelSerializer):
    number_of_lessons = SerializerMethodField()
    lessons = LessonSerializers(many=True, read_only=True)

    def get_number_of_lessons(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = ['id', 'title', 'preview', 'description', 'number_of_lessons', 'lessons']

