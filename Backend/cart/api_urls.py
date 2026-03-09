from django.urls import path
from . import api_views

urlpatterns = [
    path("", api_views.get_cart, name="get_cart"),
    path("items/", api_views.add_to_cart, name="add_to_cart"),
    path("items/<int:item_id>/", api_views.update_cart_item, name="update_cart_item"),
    path("items/<int:item_id>/remove/", api_views.remove_from_cart, name="remove_from_cart"),
    path("clear/", api_views.clear_cart, name="clear_cart"),
]