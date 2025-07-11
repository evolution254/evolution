"""
Serializers for products app.
"""
from rest_framework import serializers
from .models import Product, ProductImage, ProductLike
from apps.categories.serializers import CategorySerializer


class ProductImageSerializer(serializers.ModelSerializer):
    """
    Serializer for product images.
    """
    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'alt_text', 'order')


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for products.
    """
    images = ProductImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    seller_name = serializers.CharField(source='seller.display_name', read_only=True)
    seller_rating = serializers.DecimalField(
        source='seller.seller_rating', 
        max_digits=3, 
        decimal_places=2, 
        read_only=True
    )
    category_name = serializers.CharField(source='category.name', read_only=True)
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = (
            'id', 'title', 'description', 'price', 'condition', 'category',
            'category_name', 'seller', 'seller_name', 'seller_rating',
            'location', 'is_active', 'is_sold', 'is_featured', 'is_boosted',
            'views', 'likes', 'images', 'uploaded_images', 'tags',
            'created_at', 'updated_at', 'is_liked'
        )
        read_only_fields = ('seller', 'views', 'likes', 'created_at', 'updated_at')

    def get_is_liked(self, obj):
        """Check if current user has liked this product."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return ProductLike.objects.filter(
                product=obj, 
                user=request.user
            ).exists()
        return False

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        tags = validated_data.pop('tags', [])
        
        # Set seller to current user
        validated_data['seller'] = self.context['request'].user
        
        product = Product.objects.create(**validated_data)
        
        # Add tags
        if tags:
            product.tags.set(tags)
        
        # Create product images
        for index, image in enumerate(uploaded_images):
            ProductImage.objects.create(
                product=product,
                image=image,
                order=index
            )
        
        return product

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        tags = validated_data.pop('tags', None)
        
        # Update product fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update tags
        if tags is not None:
            instance.tags.set(tags)
        
        # Add new images if provided
        if uploaded_images:
            current_count = instance.images.count()
            for index, image in enumerate(uploaded_images):
                ProductImage.objects.create(
                    product=instance,
                    image=image,
                    order=current_count + index
                )
        
        return instance


class ProductListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for product lists.
    """
    main_image = serializers.SerializerMethodField()
    seller_name = serializers.CharField(source='seller.display_name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Product
        fields = (
            'id', 'title', 'price', 'condition', 'category_name',
            'seller_name', 'location', 'is_featured', 'is_boosted',
            'views', 'likes', 'main_image', 'created_at'
        )

    def get_main_image(self, obj):
        """Get the main product image URL."""
        main_image = obj.main_image
        if main_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(main_image.image.url)
            return main_image.image.url
        return None


class ProductLikeSerializer(serializers.ModelSerializer):
    """
    Serializer for product likes.
    """
    class Meta:
        model = ProductLike
        fields = ('id', 'product', 'user', 'created_at')
        read_only_fields = ('user', 'created_at')