"""
Views for categories app.
"""
from rest_framework import generics, permissions
from .models import Category
from .serializers import CategorySerializer, CategoryTreeSerializer


class CategoryListView(generics.ListAPIView):
    """
    List all active categories.
    """
    queryset = Category.objects.filter(is_active=True).order_by('order', 'name')
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class CategoryTreeView(generics.ListAPIView):
    """
    Get category tree structure.
    """
    queryset = Category.objects.filter(is_active=True, parent=None).order_by('order', 'name')
    serializer_class = CategoryTreeSerializer
    permission_classes = [permissions.AllowAny]


class CategoryDetailView(generics.RetrieveAPIView):
    """
    Get category details.
    """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'