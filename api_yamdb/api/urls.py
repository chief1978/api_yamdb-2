from django.urls import path

from . import views

urlpatterns = [
    path('v1/auth/signup/', views.send_confirmation_code, name='signup'),
    path('v1/auth/token/', views.get_token, name='token'),
]
