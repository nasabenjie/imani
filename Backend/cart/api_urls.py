from django.urls import path
from . import api_views

urlpatterns = [

    path("", api_views.get_cart, name="get_cart"),

    path("items/", api_views.add_to_cart, name="add_to_cart"),

]