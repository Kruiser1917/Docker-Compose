from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """
    Разрешение для модераторов.
    Проверяет, состоит ли пользователь в группе "Moderators".
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='Moderators').exists()


class IsOwner(BasePermission):
    """
    Разрешение для владельцев объектов.
    Проверяет, является ли пользователь владельцем объекта.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
