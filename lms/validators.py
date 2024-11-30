from django.core.exceptions import ValidationError
import re


def validate_video_url(value):
    """
    Валидатор для проверки, что ссылка ведет только на YouTube.
    """
    # Регулярное выражение для проверки YouTube URL
    youtube_regex = r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$'

    # Проверяем, соответствует ли переданное значение YouTube URL
    if not re.match(youtube_regex, value):
        raise ValidationError("Допускаются только ссылки на YouTube.")
