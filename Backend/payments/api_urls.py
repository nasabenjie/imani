from django.urls import path
from . import api_views

urlpatterns = [
    path("initiate/", api_views.initiate_payment, name="initiate_payment"),
    path("<int:payment_id>/check/", api_views.check_payment, name="check_payment"),
    path("history/", api_views.payment_history, name="payment_history"),

    # Webhook callbacks from MTN and Airtel
    path("callbacks/mtn/", api_views.mtn_callback, name="mtn_callback"),
    path("callbacks/airtel/", api_views.airtel_callback, name="airtel_callback"),
]