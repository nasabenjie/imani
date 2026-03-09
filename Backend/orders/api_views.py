from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.shortcuts import get_object_or_404

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

    # Get user's active cart
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

    # Check cart has items
    cart_items = cart.items.all()
    if not cart_items.exists():
        return Response(
            {"error": "Cart is empty"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Get supermarket
    supermarket = get_object_or_404(Supermarket, id=data["supermarket"])

    # Calculate totals
    subtotal = sum(item.total_price for item in cart_items)
    delivery_fee = data["delivery_fee"]
    total = subtotal + delivery_fee

    # Create order atomically — if anything fails, nothing is saved
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

        # Create order items — snapshot product name and price
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

        OrderItem.objects.bulk_create(order_items)  # single DB query for all items

        # Deactivate cart
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