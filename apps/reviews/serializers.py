"""
Serializers for reviews app.
"""
from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for reviews.
    """
    reviewer_name = serializers.CharField(source='reviewer.display_name', read_only=True)
    reviewer_avatar = serializers.ImageField(source='reviewer.avatar', read_only=True)

    class Meta:
        model = Review
        fields = (
            'id', 'product', 'reviewer', 'reviewer_name', 'reviewer_avatar',
            'seller', 'rating', 'title', 'comment', 'is_verified_purchase',
            'created_at', 'updated_at'
        )
        read_only_fields = ('reviewer', 'seller', 'created_at', 'updated_at')

    def create(self, validated_data):
        validated_data['reviewer'] = self.context['request'].user
        validated_data['seller'] = validated_data['product'].seller
        return super().create(validated_data)