from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_name",
            "unit_price",
            "quantity",
            "total_price",
        ]
        read_only_fields = ["product_name", "unit_price", "total_price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    payment_status_display = serializers.CharField(source="get_payment_status_display", read_only=True)
    payment_method_display = serializers.CharField(source="get_payment_method_display", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "supermarket",
            "status",
            "status_display",
            "payment_status",
            "payment_status_display",
            "payment_method",
            "payment_method_display",
            "payment_reference",
            "delivery_address",
            "delivery_phone",
            "delivery_notes",
            "subtotal",
            "delivery_fee",
            "total",
            "item_count",
            "items",
            "created_at",
            "updated_at",
            "delivered_at",
        ]
        read_only_fields = [
            "status",
            "payment_status",
            "payment_reference",
            "subtotal",
            "total",
            "created_at",
            "updated_at",
            "delivered_at",
        ]


class PlaceOrderSerializer(serializers.Serializer):
    """Used when placing a new order from cart."""
    supermarket = serializers.IntegerField()
    delivery_address = serializers.CharField()
    delivery_phone = serializers.CharField()
    delivery_notes = serializers.CharField(required=False, allow_blank=True, default="")
    payment_method = serializers.ChoiceField(choices=Order.PaymentMethod.choices)
    delivery_fee = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)