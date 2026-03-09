from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import api_views

urlpatterns = [
    path("register/", api_views.register, name="register"),
    path("login/", api_views.login, name="login"),
    path("me/", api_views.me, name="me"),
    path("logout/", api_views.logout, name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]