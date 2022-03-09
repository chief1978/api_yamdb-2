from rest_framework import permissions


class IsAuthorOrReadOnlyPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == "POST":
            return request.user.is_authenticated()

        return (
            obj.author == request.user
            or request.user.USER_ROLE == 'admin'
            or request.user.USER_ROLE == 'moderator')
