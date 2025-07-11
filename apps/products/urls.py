"""
URL configuration for products app.
"""
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListCreateView.as_view(), name='product-list-create'),
    path('<uuid:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('my-products/', views.MyProductsView.as_view(), name='my-products'),
    path('featured/', views.FeaturedProductsView.as_view(), name='featured-products'),
    path('trending/', views.TrendingProductsView.as_view(), name='trending-products'),
    path('<uuid:product_id>/like/', views.toggle_like, name='toggle-like'),
    path('<uuid:product_id>/sold/', views.mark_as_sold, name='mark-as-sold'),
]