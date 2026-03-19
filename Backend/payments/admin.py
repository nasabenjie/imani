from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "order",
        "user",
        "provider",
        "status",
        "amount",
        "phone",
        "internal_reference",
        "created_at",
    ]
    list_filter = ["provider", "status"]
    search_fields = [
        "user__email",
        "phone",
        "internal_reference",
        "provider_reference",
        "order__id",
    ]
    readonly_fields = [
        "order",
        "user",
        "provider",
        "amount",
        "currency",
        "phone",
        "internal_reference",
        "provider_reference",
        "provider_response",
        "created_at",
        "updated_at",
    ]
    ordering = ["-created_at"]