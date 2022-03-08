from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'genres', views.GenreViewSet)
router.register(r'titles', views.TitleViewSet, basename='titles')
router.register(r'users', views.UsersViewSet)

urlpatterns = [
    path('v1/auth/signup/', views.send_confirmation_code, name='signup'),
    path('v1/auth/token/', views.get_token, name='token'),
    path('v1/', include(router.urls)),
]
