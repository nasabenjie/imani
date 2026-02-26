from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


@api_view(["GET"])
def get_products(request):

    queryset = Product.objects.all()

    supermarket_id = request.GET.get("supermarket")
    category_id = request.GET.get("category")

    if supermarket_id:
        queryset = queryset.filter(supermarket_id=supermarket_id)

    if category_id:
        queryset = queryset.filter(category_id=category_id)

    serializer = ProductSerializer(queryset, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_categories(request):

    queryset = Category.objects.all()

    serializer = CategorySerializer(queryset, many=True)

    return Response(serializer.data)