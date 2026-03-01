from django.urls import path
from .api_views import get_products, get_categories

urlpatterns = [
    path("", get_products, name="get_products"),
    path("categories/", get_categories, name="get_categories"),
]