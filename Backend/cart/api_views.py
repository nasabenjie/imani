from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Cart, CartItem
from .serializers import CartSerializer

from products.models import Product


@api_view(["GET"])
def get_cart(request):
    """
    Get user's cart using user_id from query params (temporary, until authentication is added)
    """

    user_id = request.query_params.get("user_id")

    if not user_id:
        return Response(
            {"error": "user_id required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    cart, created = Cart.objects.get_or_create(
        user_id=user_id,
        is_active=True
    )

    serializer = CartSerializer(cart)

    return Response(serializer.data)


@api_view(["POST"])
def add_to_cart(request):
    """
    Add product to cart
    """

    user_id = request.data.get("user_id")
    product_id = request.data.get("product_id")
    quantity = int(request.data.get("quantity", 1))

    if not user_id or not product_id:
        return Response(
            {"error": "user_id and product_id required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    cart, created = Cart.objects.get_or_create(
        user_id=user_id,
        is_active=True
    )

    product = Product.objects.get(id=product_id)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity

    cart_item.save()

    serializer = CartSerializer(cart)

    return Response(serializer.data)