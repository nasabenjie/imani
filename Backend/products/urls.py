from django.urls import path
from .api_views import get_products, get_categories

urlpatterns = [
    path("products/", get_products),
    path("categories/", get_categories),
]