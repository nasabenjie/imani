from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from .models import Product
from .serializers import ProductSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def list_products(request):
    """List products, optionally filtered by supermarket."""
    supermarket_id = request.query_params.get("supermarket")

    products = Product.objects.select_related("category", "supermarket")

    if supermarket_id:
        products = products.filter(supermarket_id=supermarket_id)

    serializer = ProductSerializer(products, many=True, context={"request": request})
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def product_detail(request, product_id):
    """Get a single product."""
    try:
        product = Product.objects.select_related("category", "supermarket").get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(product, context={"request": request})
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAdminUser])
@parser_classes([MultiPartParser, FormParser])
def upload_product_image(request, product_id):
    """
    Upload an image for a product.
    Admin only. Accepts multipart/form-data with an 'image' field.
    """
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    image = request.FILES.get("image")
    if not image:
        return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)

    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/webp"]
    if image.content_type not in allowed_types:
        return Response(
            {"error": "Only JPEG, PNG and WebP images are allowed"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Validate file size (max 5MB)
    if image.size > 5 * 1024 * 1024:
        return Response(
            {"error": "Image must be under 5MB"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Delete old image if exists
    if product.image:
        product.image.delete(save=False)

    product.image = image
    product.save()

    serializer = ProductSerializer(product, context={"request": request})
    return Response(serializer.data)