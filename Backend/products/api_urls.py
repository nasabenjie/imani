from django.urls import path
from . import api_views

urlpatterns = [
    path("", api_views.list_products, name="list_products"),
    path("<int:product_id>/", api_views.product_detail, name="product_detail"),
    path("<int:product_id>/image/", api_views.upload_product_image, name="upload_product_image"),
]