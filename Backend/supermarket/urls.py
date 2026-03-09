from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path("api/auth/", include("users.api_urls")),
    path("api/products/", include("products.api_urls")),
    path("api/cart/", include("cart.api_urls")),
    path("api/supermarkets/", include("supermarkets.api_urls")),
]
