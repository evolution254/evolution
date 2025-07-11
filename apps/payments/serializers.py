"""
Serializers for payments app.
"""
from rest_framework import serializers
from .models import Payment, BoostPackage


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for payments.
    """
    class Meta:
        model = Payment
        fields = (
            'id', 'user', 'product', 'amount', 'currency', 'status',
            'stripe_payment_intent_id', 'description', 'created_at'
        )
        read_only_fields = ('user', 'created_at')


class BoostPackageSerializer(serializers.ModelSerializer):
    """
    Serializer for boost packages.
    """
    class Meta:
        model = BoostPackage
        fields = (
            'id', 'name', 'description', 'price', 'duration_days', 'is_active'
        )