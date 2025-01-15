from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Модель кастомного пользователя"""
    username = models.CharField(max_length=50, verbose_name='username', help_text='Введите имя пользователя')
    email = models.EmailField(unique=True, verbose_name='Email', help_text='Введите свой email')
    phone_number = models.CharField(max_length=15, verbose_name='Телефон', blank=True, null=True,
                                    help_text='Введите номер телефона')
    avatar = models.ImageField(upload_to='photo/avatar', blank=True, null=True, verbose_name='Аватар',
                               help_text='Загрузите аватар')
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name='Страна', help_text='Укажите страну')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class Payments(models.Model):
    """Модель платежа пользователя"""
    PAYMENT_METHOD_CHOICES = [("наличные", "наличные"), ("перевод на счет", "перевод на счет")]

    owner = models.ForeignKey(CustomUser, verbose_name="Владелец", blank=True, null=True,
                              related_name='payment_history', on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")
    paid_course = models.ForeignKey('course_platform.Course', null=True, blank=True, on_delete=models.CASCADE,
                                    verbose_name="Оплаченный курс")
    paid_lesson = models.ForeignKey('course_platform.Lesson', null=True, blank=True, on_delete=models.CASCADE,
                                    verbose_name="Оплаченный урок")
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма оплаты")
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, verbose_name="способ оплаты")

    def __str__(self):
        return f'{self.owner} - {self.payment_amount} - {self.payment_date}'

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["-payment_date"]
