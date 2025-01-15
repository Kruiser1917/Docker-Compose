from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from course_platform.models import Course, Lesson
from users.models import CustomUser, Payments
from rest_framework_simplejwt.tokens import AccessToken
from users.services import create_stripe_product, create_stripe_price


class UserProfileViewSetTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='password', email='test1@test.com')
        self.client.force_authenticate(user=self.user)

    def test_get_user_profile(self):
        """Тест вывода детализации пользователя"""
        url = reverse('users:userprofile-detail', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_update_user_profile(self):
        """Тест обновления данных пользователя"""
        url = reverse('users:userprofile-detail', kwargs={'pk': self.user.pk})
        data = {'username': 'updateduser',
                'password': 'password',
                'email': 'test4@tast.com'
                }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')


class PaymentsViewSetTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='password')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title='course1', description='test1')
        self.lesson = Lesson.objects.create(title='lesson1', description='test1', course=self.course)

        self.payment = Payments.objects.create(
            payment_method='credit_card',
            payment_amount=10,
            paid_course=self.course,
            paid_lesson=self.lesson,
            payment_date='2023-01-01'
        )

    def test_list_payments(self):
        """Тест вывода платежа"""
        url = reverse('users:payments-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # def test_payments_create(self):
    #     """Тест создания платежа"""
    #     url = reverse('users:payments-list')
    #     course2 = Course.objects.create(title='course2', description='test1')
    #     lesson2 = Lesson.objects.create(title='lesson2', description='test1', course=self.course)
    #
    #     data = {
    #         'payment_method': "наличные",
    #         'payment_amount': 10,
    #         'paid_course': course2.id,
    #         'paid_lesson': lesson2.id,
    #         'payment_date': '2023-01-02'
    #     }
    #     response = self.client.post(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Payments.objects.count(), 2)


class CustomsUserViewSetTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='password')
        self.access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token))

    def test_list_users(self):
        """Тест вывода пользователей"""
        url = reverse('users:users-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_user_detail(self):
        """Тест вывода детальной информации о пользователе"""
        url = reverse('users:users-detail', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)


class CustomUserCreateAPIViewTests(APITestCase):
    def test_create_user(self):
        """Тест создания пользователя."""
        url = reverse('users:register')
        data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'email': 'testuser@example.com'
        }
        response = self.client.post(url, data, format='json')

        # Проверяем, что пользователь был создан
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(username='testuser').exists())

    def test_create_user_invalid(self):
        """Тесть создания пользователя с некорректными данными."""
        url = reverse('users:register')
        data = {
            'username': '',
            'password': 'testpassword123',
            'email': 'testuser@example.com'
        }
        response = self.client.post(url, data, format='json')
        print(response.status_code)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PaymentsTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email="testuser@example.com", is_active=True)
        self.user.set_password("testpassword")
        self.user.save()

        self.course = Course.objects.create(title="Test Course", description="Test description", owner=self.user)

    def test_create_product(self):
        """Тестирование создания продукта в Stripe"""
        product = create_stripe_product(self.course)
        self.assertIn("id", product)

    def test_create_price(self):
        """Тестирование создания цены в Stripe"""
        product = create_stripe_product(self.course)
        price = create_stripe_price(1000, product.id)
        self.assertIn("id", price)
