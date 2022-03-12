from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class IsAuthenticatedPost(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            if request.method == 'POST'
            else False
        )


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
            or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
            or request.user.is_staff
        )


class IsModeratorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.method in permissions.SAFE_METHODS:
            return request.method in permissions.SAFE_METHODS

        return request.user.role == 'moderator'

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.method in permissions.SAFE_METHODS:
            return request.method in permissions.SAFE_METHODS

        return request.user.role == 'moderator'


class IsModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == 'moderator'

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'moderator'


# class IsAuthorOrAdminOrModerator(permissions.BasePermission):

#     def has_object_permission(self, request, view, obj):
#         if request.user.is_superuser:
#             return True
#         if request.method in permissions.SAFE_METHODS:
#             return request.method in permissions.SAFE_METHODS

#         return (
#             request.user == obj.author
#             or request.user.role == 'moderator'
#             or request.user.is_superuser
#         )


class AuthorOrAdminOrModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == "POST":
            return request.user.is_authenticated
        if not request.user.is_anonymous:
            return (
                request.user.USER_ROLE == 'admin'
                or request.user.USER_ROLE == 'moderator'
            )
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == "POST":
            return request.user.is_authenticated
        return (
            obj.author == request.user
            or request.user.USER_ROLE == 'admin'
            or request.user.USER_ROLE == 'moderator'
        )
