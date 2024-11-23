from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Админ-панель
    path('admin/', admin.site.urls),

    # Маршруты для API курсов и уроков
    path('api/', include('lms.urls')),

    # Маршруты для работы с пользователями
    path('users/', include('users.urls')),
]
