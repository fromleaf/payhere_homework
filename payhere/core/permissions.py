from rest_framework import permissions


class AllowAny(permissions.AllowAny):
    pass


class IsAuthenticated(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_active
        )
