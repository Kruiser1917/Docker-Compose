from django.core.exceptions import ValidationError
from urllib.parse import urlparse

def youtube_link_validator(value):
    """
    Проверяет, что ссылка ведет на youtube.com
    """
    parsed_url = urlparse(value)
    if 'youtube.com' not in parsed_url.netloc:
        raise ValidationError("Ссылка должна вести на youtube.com")
