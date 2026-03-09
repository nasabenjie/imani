from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Cart, CartItem
from .serializers import CartSerializer
from products.models import Product


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_cart(request):
    """Get the logged in user's active cart."""
    cart, _ = Cart.objects.get_or_create(
        user=request.user,
        is_active=True
    )
    return Response(CartSerializer(cart).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    """Add a product to the logged in user's cart."""
    product_id = request.data.get("product_id")
    quantity = int(request.data.get("quantity", 1))

    if not product_id:
        return Response(
            {"error": "product_id is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response(
            {"error": "Product not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    cart, _ = Cart.objects.get_or_create(
        user=request.user,
        is_active=True
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity

    cart_item.save()

    return Response(CartSerializer(cart).data)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_cart_item(request, item_id):
    """Update quantity of a cart item."""
    quantity = request.data.get("quantity")

    if quantity is None:
        return Response(
            {"error": "quantity is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        cart_item = CartItem.objects.get(
            id=item_id,
            cart__user=request.user,
            cart__is_active=True
        )
    except CartItem.DoesNotExist:
        return Response(
            {"error": "Cart item not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    quantity = int(quantity)
    if quantity <= 0:
        cart_item.delete()
    else:
        cart_item.quantity = quantity
        cart_item.save()

    cart = Cart.objects.get(user=request.user, is_active=True)
    return Response(CartSerializer(cart).data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, item_id):
    """Remove a specific item from the cart."""
    try:
        cart_item = CartItem.objects.get(
            id=item_id,
            cart__user=request.user,
            cart__is_active=True
        )
    except CartItem.DoesNotExist:
        return Response(
            {"error": "Cart item not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    cart_item.delete()
    cart = Cart.objects.get(user=request.user, is_active=True)
    return Response(CartSerializer(cart).data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def clear_cart(request):
    """Remove all items from the cart."""
    try:
        cart = Cart.objects.get(user=request.user, is_active=True)
        cart.items.all().delete()
        return Response(CartSerializer(cart).data)
    except Cart.DoesNotExist:
        return Response({"error": "No active cart found"}, status=status.HTTP_404_NOT_FOUND)