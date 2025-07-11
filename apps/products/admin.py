"""
Admin configuration for products app.
"""
from django.contrib import admin
from .models import Product, ProductImage, ProductLike


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text', 'order')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'seller', 'category', 'price', 'condition', 
        'is_active', 'is_sold', 'is_featured', 'views', 'created_at'
    )
    list_filter = (
        'condition', 'is_active', 'is_sold', 'is_featured', 'is_boosted',
        'category', 'created_at'
    )
    search_fields = ('title', 'description', 'seller__email', 'seller__username')
    readonly_fields = ('views', 'likes', 'created_at', 'updated_at')
    inlines = [ProductImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'price', 'condition', 'category', 'seller')
        }),
        ('Location', {
            'fields': ('location', 'latitude', 'longitude')
        }),
        ('Status', {
            'fields': ('is_active', 'is_sold', 'is_featured', 'is_boosted', 'boost_expires_at')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Analytics', {
            'fields': ('views', 'likes'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt_text', 'order', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('product__title', 'alt_text')


@admin.register(ProductLike)
class ProductLikeAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('product__title', 'user__email')