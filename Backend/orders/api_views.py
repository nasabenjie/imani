from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Order, OrderItem
from .serializers import OrderSerializer, PlaceOrderSerializer
from cart.models import Cart
from supermarkets.models import Supermarket


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_orders(request):
    """List all orders for the logged in user."""
    orders = Order.objects.filter(user=request.user).prefetch_related("items")
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def order_detail(request, order_id):
    """Get a single order."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    serializer = OrderSerializer(order)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def place_order(request):
    """
    Place a new order from the user's active cart.
    Clears the cart after order is placed.
    """
    serializer = PlaceOrderSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data

    try:
        cart = Cart.objects.prefetch_related("items__product").get(
            user=request.user,
            is_active=True
        )
    except Cart.DoesNotExist:
        return Response(
            {"error": "No active cart found"},
            status=status.HTTP_400_BAD_REQUEST
        )

    cart_items = cart.items.all()
    if not cart_items.exists():
        return Response(
            {"error": "Cart is empty"},
            status=status.HTTP_400_BAD_REQUEST
        )

    supermarket = get_object_or_404(Supermarket, id=data["supermarket"])

    subtotal = sum(item.total_price for item in cart_items)
    delivery_fee = data["delivery_fee"]
    total = subtotal + delivery_fee

    with transaction.atomic():
        order = Order.objects.create(
            user=request.user,
            supermarket=supermarket,
            delivery_address=data["delivery_address"],
            delivery_phone=data["delivery_phone"],
            delivery_notes=data.get("delivery_notes", ""),
            payment_method=data["payment_method"],
            subtotal=subtotal,
            delivery_fee=delivery_fee,
            total=total,
        )

        order_items = []
        for cart_item in cart_items:
            order_items.append(OrderItem(
                order=order,
                product=cart_item.product,
                product_name=cart_item.product.name,
                unit_price=cart_item.product.price,
                quantity=cart_item.quantity,
                total_price=cart_item.total_price,
            ))

        OrderItem.objects.bulk_create(order_items)

        cart.is_active = False
        cart.save()

    return Response(
        OrderSerializer(order).data,
        status=status.HTTP_201_CREATED
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cancel_order(request, order_id):
    """Cancel a pending order."""
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status not in [Order.Status.PENDING, Order.Status.CONFIRMED]:
        return Response(
            {"error": f"Cannot cancel order with status '{order.status}'"},
            status=status.HTTP_400_BAD_REQUEST
        )

    order.status = Order.Status.CANCELLED
    order.save()

    return Response({"message": "Order cancelled successfully"})


# ─── Admin / Staff Endpoints ─────────────────────────────────────────────────

# Valid status transitions — prevents jumping to invalid states
VALID_TRANSITIONS = {
    Order.Status.PENDING: [Order.Status.CONFIRMED, Order.Status.CANCELLED],
    Order.Status.CONFIRMED: [Order.Status.PREPARING, Order.Status.CANCELLED],
    Order.Status.PREPARING: [Order.Status.OUT_FOR_DELIVERY],
    Order.Status.OUT_FOR_DELIVERY: [Order.Status.DELIVERED],
    Order.Status.DELIVERED: [],
    Order.Status.CANCELLED: [],
}


@api_view(["POST"])
@permission_classes([IsAdminUser])
def update_order_status(request, order_id):
    """
    Update the status of an order. Admin only.
    Enforces valid status transitions.
    """
    order = get_object_or_404(Order, id=order_id)
    new_status = request.data.get("status")

    if not new_status:
        return Response(
            {"error": "status is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check it's a valid status value
    valid_statuses = [s.value for s in Order.Status]
    if new_status not in valid_statuses:
        return Response(
            {"error": f"Invalid status. Choose from: {', '.join(valid_statuses)}"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check transition is allowed
    allowed = VALID_TRANSITIONS.get(order.status, [])
    if new_status not in allowed:
        return Response(
            {
                "error": f"Cannot move order from '{order.status}' to '{new_status}'",
                "allowed_transitions": allowed,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    order.status = new_status

    # Set delivered_at timestamp when order is delivered
    if new_status == Order.Status.DELIVERED:
        order.delivered_at = timezone.now()

    order.save()

    return Response(OrderSerializer(order).data)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def admin_list_orders(request):
    """
    List all orders. Admin only.
    Supports filtering by status, supermarket, and payment_status.
    """
    orders = Order.objects.prefetch_related("items").select_related("user", "supermarket")

    # Optional filters
    order_status = request.query_params.get("status")
    supermarket_id = request.query_params.get("supermarket")
    payment_status = request.query_params.get("payment_status")

    if order_status:
        orders = orders.filter(status=order_status)
    if supermarket_id:
        orders = orders.filter(supermarket_id=supermarket_id)
    if payment_status:
        orders = orders.filter(payment_status=payment_status)

    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)