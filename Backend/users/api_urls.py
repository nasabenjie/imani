from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import api_views

urlpatterns = [
    path("register/", api_views.register, name="register"),
    path("login/", api_views.login, name="login"),
    path("me/", api_views.me, name="me"),
    path("logout/", api_views.logout, name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Password reset
    path("forgot-password/", api_views.forgot_password, name="forgot_password"),
    path("reset-password/", api_views.reset_password, name="reset_password"),
    path("change-password/", api_views.change_password, name="change_password"),
]