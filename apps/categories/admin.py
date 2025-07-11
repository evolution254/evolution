"""
Admin configuration for categories app.
"""
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ('name', 'parent', 'is_active', 'order', 'product_count')
    list_filter = ('is_active', 'parent')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active', 'order')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'parent')
        }),
        ('Display', {
            'fields': ('icon', 'image', 'order', 'is_active')
        }),
    )