from rest_framework import permissions

from recipe.models import User


class AuthorOrModeratorOrAdminOrReadonly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user == obj.author
            or request.user.role == User.Admin
            or request.user.is_superuser
        )


class Admin(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            and request.user.role == User.Admin
            or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            and request.user.role == User.Admin
            or request.user.is_superuser
        )


