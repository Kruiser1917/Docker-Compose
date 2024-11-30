from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Course, Lesson, Subscription

User = get_user_model()


class LessonTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title="Test Course", description="Description", owner=self.user)

    def test_lesson_creation(self):
        data = {
            "title": "Test Lesson",
            "course": self.course.id,
            "video_url": "https://youtube.com/test",
            "description": "Lesson description"
        }
        response = self.client.post("/api/lessons/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_video_url(self):
        data = {
            "title": "Test Lesson",
            "course": self.course.id,
            "video_url": "https://example.com/invalid",
            "description": "Lesson description"
        }
        response = self.client.post("/api/lessons/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SubscriptionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title="Test Course", description="Description", owner=self.user)

    def test_add_subscription(self):
        data = {"course_id": self.course.id}
        response = self.client.post("/api/subscriptions/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_remove_subscription(self):
        Subscription.objects.create(user=self.user, course=self.course)
        data = {"course_id": self.course.id}
        response = self.client.post("/api/subscriptions/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
