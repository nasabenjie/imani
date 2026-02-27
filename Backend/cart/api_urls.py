from django.urls import path
from .api_views import *

urlpatterns = [
    path("add/", add_to_cart),
    path("user/<int:user_id>/", get_user_cart),
]