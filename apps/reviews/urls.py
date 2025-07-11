"""
URL configuration for reviews app.
"""
from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.ReviewListCreateView.as_view(), name='review-list-create'),
    path('<uuid:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),
]