from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.method in permissions.SAFE_METHODS:
            return request.method in permissions.SAFE_METHODS

        return request.user.role == 'admin'

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.method in permissions.SAFE_METHODS:
            return request.method in permissions.SAFE_METHODS

        return request.user.role == 'admin'


class IsModeratorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.method in permissions.SAFE_METHODS:
            return request.method in permissions.SAFE_METHODS

        return request.user.role == 'moderator'

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.method in permissions.SAFE_METHODS:
            return request.method in permissions.SAFE_METHODS

        return request.user.role == 'moderator'


class IsAuthorOrAdminOrModerator(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.method in permissions.SAFE_METHODS:
            return request.method in permissions.SAFE_METHODS

        return (
            request.user == obj.author
            or request.user.role == 'admin'
            or request.user.role == 'moderator'
        )


class AuthorOrAdminOrModerator(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == "POST":
            return request.user.is_authenticated()
        return (
            obj.author == request.user
            or request.user.USER_ROLE == 'admin'
            or request.user.USER_ROLE == 'moderator'
        )


class IsAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            (request.user and request.user.is_staff)
            or request.user.is_superuser
        )
