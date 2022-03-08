from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class MixinUsersViewset(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    """
    A viewset that provides default `create()` and `list()` actions.
    """
    pass
