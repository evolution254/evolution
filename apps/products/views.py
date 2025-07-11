"""
Views for products app.
"""
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from .models import Product, ProductLike
from .serializers import ProductSerializer, ProductListSerializer, ProductLikeSerializer
from .filters import ProductFilter
from apps.core.permissions import IsOwnerOrReadOnly, CanCreateProduct


class ProductListCreateView(generics.ListCreateAPIView):
    """
    List all products or create a new product.
    """
    queryset = Product.objects.filter(is_active=True, is_deleted=False)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CanCreateProduct]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'description', 'tags__name']
    ordering_fields = ['price', 'created_at', 'views', 'likes']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductListSerializer
        return ProductSerializer


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a product.
    """
    queryset = Product.objects.filter(is_active=True, is_deleted=False)
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment views if not the owner
        if not request.user.is_authenticated or request.user != instance.seller:
            instance.increment_views()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class MyProductsView(generics.ListAPIView):
    """
    List current user's products.
    """
    serializer_class = ProductListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(
            seller=self.request.user,
            is_deleted=False
        ).order_by('-created_at')


class FeaturedProductsView(generics.ListAPIView):
    """
    List featured products.
    """
    queryset = Product.objects.filter(
        is_active=True,
        is_featured=True,
        is_deleted=False
    ).order_by('-created_at')
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]


class TrendingProductsView(generics.ListAPIView):
    """
    List trending products (most viewed).
    """
    queryset = Product.objects.filter(
        is_active=True,
        is_deleted=False
    ).order_by('-views', '-created_at')[:20]
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def toggle_like(request, product_id):
    """
    Toggle like/unlike for a product.
    """
    try:
        product = Product.objects.get(id=product_id, is_active=True)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    like, created = ProductLike.objects.get_or_create(
        product=product,
        user=request.user
    )

    if not created:
        like.delete()
        product.likes -= 1
        product.save(update_fields=['likes'])
        return Response({'liked': False, 'likes_count': product.likes})
    else:
        product.likes += 1
        product.save(update_fields=['likes'])
        return Response({'liked': True, 'likes_count': product.likes})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_as_sold(request, product_id):
    """
    Mark product as sold.
    """
    try:
        product = Product.objects.get(id=product_id, seller=request.user)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    product.mark_as_sold()
    return Response({'message': 'Product marked as sold'})