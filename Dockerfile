# Используем официальный Python образ
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимые файлы
COPY requirements.txt .

# Устанавливаем зависимости с явным указанием источника
RUN pip install --no-cache-dir -r requirements.txt --index-url https://pypi.org/simple

# Копируем весь проект в контейнер
COPY . .

# Открываем порт для Django
EXPOSE 8000

# Используем Gunicorn для продакшн-сервера
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "habit_tracker.wsgi:application"]
