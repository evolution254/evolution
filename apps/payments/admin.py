"""
Admin configuration for payments app.
"""
from django.contrib import admin
from .models import Payment, BoostPackage


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'product', 'amount', 'currency', 
        'status', 'created_at'
    )
    list_filter = ('status', 'currency', 'created_at')
    search_fields = ('user__email', 'stripe_payment_intent_id', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(BoostPackage)
class BoostPackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_days', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')