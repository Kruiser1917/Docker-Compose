from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.shortcuts import redirect

def home(request):
    return HttpResponse("<h1>Welcome to the Django DRF Project</h1>")

urlpatterns = [
    path('', lambda request: redirect('api/', permanent=True)),  # Перенаправляет на /api/
    path('api/', include('lms.urls')),  # Ваши API маршруты
    path('admin/', admin.site.urls),    # Админ-панель
    path('api/', include('users.urls')),
]
