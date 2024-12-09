from celery import shared_task
from django.utils.timezone import now, timedelta
from .models import CustomUser

@shared_task
def deactivate_inactive_users():
    one_month_ago = now() - timedelta(days=30)
    inactive_users = CustomUser.objects.filter(last_login__lt=one_month_ago, is_active=True)
    inactive_users.update(is_active=False)
