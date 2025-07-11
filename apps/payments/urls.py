"""
URL configuration for payments app.
"""
from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.PaymentListView.as_view(), name='payment-list'),
    path('boost-packages/', views.BoostPackageListView.as_view(), name='boost-package-list'),
    path('create-intent/', views.create_payment_intent, name='create-payment-intent'),
]