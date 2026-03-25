from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from .models import Supermarket
from .serializers import SupermarketSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def supermarket_list(request):
    supermarkets = Supermarket.objects.all()
    serializer = SupermarketSerializer(supermarkets, many=True, context={"request": request})
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def supermarket_detail(request, pk):
    supermarket = get_object_or_404(Supermarket, pk=pk)
    serializer = SupermarketSerializer(supermarket, context={"request": request})
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAdminUser])
@parser_classes([MultiPartParser, FormParser])
def upload_supermarket_image(request, pk):
    """Upload an image for a supermarket. Admin only."""
    supermarket = get_object_or_404(Supermarket, pk=pk)

    image = request.FILES.get("image")
    if not image:
        return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)

    allowed_types = ["image/jpeg", "image/png", "image/webp"]
    if image.content_type not in allowed_types:
        return Response(
            {"error": "Only JPEG, PNG and WebP images are allowed"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if image.size > 5 * 1024 * 1024:
        return Response(
            {"error": "Image must be under 5MB"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if supermarket.image:
        supermarket.image.delete(save=False)

    supermarket.image = image
    supermarket.save()

    serializer = SupermarketSerializer(supermarket, context={"request": request})
    return Response(serializer.data)