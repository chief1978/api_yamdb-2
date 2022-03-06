from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

app_name = 'titles'

router = DefaultRouter()
router.register(r'categories', FollowViewSet)
router.register(r'genres', GroupViewSet)
router.register(r'titles', PostViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
