from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Cart, CartItem
from .serializers import CartSerializer

from django.contrib.auth import get_user_model

User = get_user_model()


@api_view(["POST"])
def add_to_cart(request):
    user_id = request.data.get("user_id")
    product_id = request.data.get("product_id")
    quantity = int(request.data.get("quantity", 1))

    if not user_id or not product_id:
        return Response(
            {"error": "user_id and product_id required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.get(id=user_id)

    cart, created = Cart.objects.get_or_create(
        user=user,
        is_active=True
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product_id=product_id,
    )

    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity

    cart_item.save()

    serializer = CartSerializer(cart)

    return Response(serializer.data)


@api_view(["GET"])
def get_user_cart(request, user_id):

    try:
        cart = Cart.objects.get(user_id=user_id, is_active=True)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    except Cart.DoesNotExist:
        return Response({
            "id": None,
            "user": user_id,
            "items": [],
            "created_at": None
        })