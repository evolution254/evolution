"""
Serializers for categories app.
"""
from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for categories.
    """
    product_count = serializers.ReadOnlyField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            'id', 'name', 'slug', 'description', 'icon', 'image',
            'parent', 'is_active', 'order', 'product_count', 'children'
        )

    def get_children(self, obj):
        """Get child categories."""
        if obj.children.exists():
            return CategorySerializer(
                obj.children.filter(is_active=True),
                many=True,
                context=self.context
            ).data
        return []


class CategoryTreeSerializer(serializers.ModelSerializer):
    """
    Serializer for category tree structure.
    """
    children = serializers.SerializerMethodField()
    product_count = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'icon', 'product_count', 'children')

    def get_children(self, obj):
        """Get child categories recursively."""
        children = obj.get_children().filter(is_active=True)
        return CategoryTreeSerializer(children, many=True, context=self.context).data