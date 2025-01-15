from celery import shared_task
from django.core.mail import send_mail
from course_platform.models import Subscription
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from config import settings


@shared_task
def send_course_update_notification(course_id):
    """Обновление курса и отправка письма с помощью функции Send_mail"""
    subscriptions = Subscription.objects.filter(course_id=course_id)
    for subscription in subscriptions:
        send_mail(
            'Курс обновлен',
            'Обновления по курсу доступны. Проверьте свои материалы!',
            settings.EMAIL_HOST_USER,
            [subscription.user.email],
            fail_silently=False,
        )


@shared_task
def block_inactive_users():
    """Проверка логирования пользователей в последние 30 дней"""
    month_ago = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=month_ago, is_active=True)
    inactive_users.update(is_active=False)
