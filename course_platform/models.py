from django.db import models

from users.models import CustomUser


class Course(models.Model):
    """Модель курса на обучающей платформе"""
    title = models.CharField(max_length=255, verbose_name='название курса')
    preview = models.ImageField(upload_to='course/photo', blank=True, null=True)
    description = models.TextField()
    owner = models.ForeignKey(
        CustomUser,
        verbose_name="Владелец",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.description}"

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'
        ordering = ['title']


class Lesson(models.Model):
    """Модель урока на обучающей платформе"""
    title = models.CharField(max_length=255, verbose_name='название курса')
    description = models.TextField()
    preview = models.ImageField(upload_to='lesson/photo', blank=True, null=True)
    link_to_video = models.URLField(max_length=200, blank=True, null=True)
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    owner = models.ForeignKey(
        CustomUser,
        verbose_name="Владелец",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return f"{self.title} - {self.description}"

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
        ordering = ['title']


class Subscription(models.Model):
    """Модель подписки на обучающей платформе"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'course')
