"""
URL configuration for categories app.
"""
from django.urls import path
from . import views

app_name = 'categories'

urlpatterns = [
    path('', views.CategoryListView.as_view(), name='category-list'),
    path('tree/', views.CategoryTreeView.as_view(), name='category-tree'),
    path('<slug:slug>/', views.CategoryDetailView.as_view(), name='category-detail'),
]