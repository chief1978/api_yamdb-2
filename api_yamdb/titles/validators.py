from rest_framework.utils.representation import smart_repr

from .exceptions import SelfFollow


class UserFollowValidator:
    """
    Проверка имя пользователя (user_field)
    не равно имени автора (following_field)
    """
    message = ('Нельзя подписаться на самого себя.')

    def __init__(
            self,
            user_field="user",
            following_field="following",
            message=None
    ):
        self.user_field = user_field
        self.following_field = following_field
        self.message = message or self.message

    def __call__(self, attrs):
        if attrs[self.user_field] == attrs[self.following_field]:
            raise SelfFollow()

    def __repr__(self):
        return '<%s(user_field=%s, following_field=%s)>' % (
            self.__class__.__name__,
            smart_repr(self.user_field),
            smart_repr(self.following_field)
        )
