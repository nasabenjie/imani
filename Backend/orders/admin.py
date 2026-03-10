from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["product", "product_name", "unit_price", "quantity", "total_price"]
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "supermarket",
        "status",
        "payment_status",
        "payment_method",
        "total",
        "item_count",
        "created_at",
    ]
    list_filter = ["status", "payment_status", "payment_method", "supermarket"]
    search_fields = ["user__email", "user__full_name", "delivery_phone", "delivery_address"]
    readonly_fields = [
        "user",
        "supermarket",
        "subtotal",
        "delivery_fee",
        "total",
        "payment_reference",
        "created_at",
        "updated_at",
    ]
    ordering = ["-created_at"]
    inlines = [OrderItemInline]

    fieldsets = (
        ("Order Info", {
            "fields": ("user", "supermarket", "status")
        }),
        ("Delivery", {
            "fields": ("delivery_address", "delivery_phone", "delivery_notes")
        }),
        ("Payment", {
            "fields": ("payment_method", "payment_status", "payment_reference")
        }),
        ("Financials", {
            "fields": ("subtotal", "delivery_fee", "total")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at", "delivered_at")
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["id", "order", "product_name", "unit_price", "quantity", "total_price"]
    search_fields = ["product_name", "order__id"]
    readonly_fields = ["order", "product", "product_name", "unit_price", "quantity", "total_price"]