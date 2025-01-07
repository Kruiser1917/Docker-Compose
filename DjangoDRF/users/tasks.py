from celery import shared_task
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import timedelta

@shared_task
def block_inactive_users():
    """Блокирует пользователей, которые не заходили больше месяца."""
    threshold_date = now() - timedelta(days=30)
    User.objects.filter(last_login__lt=threshold_date, is_active=True).update(is_active=False)
