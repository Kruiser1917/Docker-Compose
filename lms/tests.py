from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Course, Lesson, Subscription

User = get_user_model()

class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title="Test Course", owner=self.user)
        self.lesson = Lesson.objects.create(title="Test Lesson", course=self.course, video_url="https://youtube.com/test")

    def test_lesson_creation(self):
        response = self.client.post('/api/lessons/', {
            "title": "New Lesson",
            "course": self.course.id,
            "video_url": "https://youtube.com/newlesson"
        })
        self.assertEqual(response.status_code, 201)

    def test_invalid_video_url(self):
        response = self.client.post('/api/lessons/', {
            "title": "Invalid URL Lesson",
            "course": self.course.id,
            "video_url": "https://otherplatform.com/lesson"
        })
        self.assertEqual(response.status_code, 400)

class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title="Test Course", owner=self.user)

    def test_add_subscription(self):
        response = self.client.post('/subscriptions/', {"course_id": self.course.id})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Подписка добавлена", response.data["message"])

    def test_remove_subscription(self):
        Subscription.objects.create(user=self.user, course=self.course)
        response = self.client.post('/subscriptions/', {"course_id": self.course.id})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Подписка удалена", response.data["message"])
