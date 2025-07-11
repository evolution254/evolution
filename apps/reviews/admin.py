"""
Admin configuration for reviews app.
"""
from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'product', 'reviewer', 'seller', 'rating', 
        'is_verified_purchase', 'created_at'
    )
    list_filter = ('rating', 'is_verified_purchase', 'created_at')
    search_fields = (
        'product__title', 'reviewer__email', 'seller__email', 
        'title', 'comment'
    )
    readonly_fields = ('created_at', 'updated_at')