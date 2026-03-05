from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Supermarket
from .serializers import SupermarketSerializer


@api_view(["GET"])
def supermarket_list(request):
    supermarkets = Supermarket.objects.all()
    serializer = SupermarketSerializer(supermarkets, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def supermarket_detail(request, pk):
    supermarket = get_object_or_404(Supermarket, pk=pk)
    serializer = SupermarketSerializer(supermarket)
    return Response(serializer.data)