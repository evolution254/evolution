"""
Filters for products app.
"""
import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    """
    Filter for products.
    """
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    condition = django_filters.ChoiceFilter(choices=Product.CONDITION_CHOICES)
    location = django_filters.CharFilter(field_name='location', lookup_expr='icontains')
    is_featured = django_filters.BooleanFilter()
    
    class Meta:
        model = Product
        fields = ['min_price', 'max_price', 'category', 'condition', 'location', 'is_featured']