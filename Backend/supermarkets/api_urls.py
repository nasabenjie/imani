from django.urls import path
from . import api_views

urlpatterns = [
    path("", api_views.supermarket_list, name="supermarket-list"),
    path("<int:pk>/", api_views.supermarket_detail, name="supermarket-detail"),
    path("<int:pk>/image/", api_views.upload_supermarket_image, name="supermarket-image"),
]