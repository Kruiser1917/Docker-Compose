from celery import shared_task
from django.core.mail import send_mail
from .models import Course, Subscription

@shared_task
def send_course_update_notification(course_id):
    try:
        course = Course.objects.get(id=course_id)
        subscribers = Subscription.objects.filter(course=course).select_related('user')
        emails = [sub.user.email for sub in subscribers if sub.user.email]

        if emails:
            send_mail(
                subject=f'Обновление курса: {course.title}',
                message=f'Материалы курса "{course.title}" были обновлены.',
                from_email='no-reply@example.com',
                recipient_list=emails,
                fail_silently=False,
            )
    except Course.DoesNotExist:
        print(f"Course with id {course_id} does not exist.")
