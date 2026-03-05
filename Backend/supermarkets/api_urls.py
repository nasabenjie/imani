from django.urls import path
from .api_views import supermarket_list, supermarket_detail

urlpatterns = [
    path("", supermarket_list, name="supermarket-list"),
    path("<int:pk>/", supermarket_detail, name="supermarket-detail"),
]