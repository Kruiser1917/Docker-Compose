import json
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    """Кастомная команда для создания фикстуры групп пользователей"""

    def handle(self, *args, **options):
        groups = Group.objects.all()
        group_data = []

        for group in groups:
            group_data.append({
                'id': group.id,
                'name': group.name,
                'permissions': [perm.codename for perm in group.permissions.all()]
            })

        with open('groups_fixture.json', 'w') as f:
            json.dump(group_data, f, indent=4)

        self.stdout.write(self.style.SUCCESS('Файл groups_fixture.json успешно создан.'))
