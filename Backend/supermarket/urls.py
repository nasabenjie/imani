from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path("api/auth/", include("users.api_urls")),
    path("api/products/", include("products.api_urls")),
    path("api/cart/", include("cart.api_urls")),
    path("api/supermarkets/", include("supermarkets.api_urls")),
    path("api/orders/", include("orders.api_urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)