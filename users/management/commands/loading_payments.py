from django.core.management.base import BaseCommand

from course_platform.models import Course, Lesson
from users.models import Payments
from django.utils import timezone


class Command(BaseCommand):
    help = "Load sample payment data"

    def handle(self, *args, **kwargs):
        course1 = Course.objects.get(id=1)
        lesson1 = Lesson.objects.get(id=2)

        sample_data = [
            {
                "user_id": 1,
                "payment_date": timezone.now(),
                "paid_course": course1,
                "paid_lesson": None,
                "payment_amount": 100.00,
                "payment_method": "наличные",
            },
            {
                "user_id": 2,
                "payment_date": timezone.now(),
                "paid_course": None,
                "paid_lesson": lesson1,
                "payment_amount": 50.00,
                "payment_method": "перевод на счет",
            }
        ]

        for item in sample_data:
            Payments.objects.create(**item)
        self.stdout.write(self.style.SUCCESS("Данные успешно загружены!"))
