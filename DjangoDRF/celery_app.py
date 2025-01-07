from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Указываем настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoDRF.settings')

# Создаем экземпляр Celery
app = Celery('DjangoDRF')

# Загружаем настройки из файла settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение задач (tasks.py в приложениях)
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
