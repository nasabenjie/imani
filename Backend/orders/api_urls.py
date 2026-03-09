from django.urls import path
from . import api_views

urlpatterns = [
    path("", api_views.list_orders, name="list_orders"),
    path("place/", api_views.place_order, name="place_order"),
    path("<int:order_id>/", api_views.order_detail, name="order_detail"),
    path("<int:order_id>/cancel/", api_views.cancel_order, name="cancel_order"),
]