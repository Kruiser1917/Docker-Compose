from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Создает группу Moderators'

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name='Moderators')
        if created:
            self.stdout.write(self.style.SUCCESS("Группа 'Moderators' успешно создана."))
        else:
            self.stdout.write(self.style.WARNING("Группа 'Moderators' уже существует."))
