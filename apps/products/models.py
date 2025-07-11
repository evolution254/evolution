"""
Product models for New Revolution marketplace.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import BaseModel, SEOModel, PublishableModel
from apps.core.utils import generate_product_image_path
from taggit.managers import TaggableManager
from mptt.models import MPTTModel, TreeForeignKey
import uuid


class Product(BaseModel, SEOModel, PublishableModel):
    """
    Product model for marketplace listings.
    """
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('used', 'Used'),
        ('refurbished', 'Refurbished'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    
    # Product details
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='used')
    category = models.ForeignKey(
        'categories.Category', 
        on_delete=models.CASCADE, 
        related_name='products'
    )
    
    # Seller information
    seller = models.ForeignKey(
        'accounts.User', 
        on_delete=models.CASCADE, 
        related_name='products'
    )
    
    # Location
    location = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True
    )
    
    # Status
    is_active = models.BooleanField(default=True)
    is_sold = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_boosted = models.BooleanField(default=False)
    boost_expires_at = models.DateTimeField(null=True, blank=True)
    
    # Analytics
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    
    # Tags
    tags = TaggableManager(blank=True)

    class Meta:
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['seller', 'is_active']),
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['price']),
            models.Index(fields=['created_at']),
            models.Index(fields=['is_featured', 'is_active']),
            models.Index(fields=['is_boosted', 'boost_expires_at']),
        ]

    def __str__(self):
        return self.title

    @property
    def main_image(self):
        """Get the main product image."""
        return self.images.first()

    @property
    def image_count(self):
        """Get the number of images."""
        return self.images.count()

    def increment_views(self):
        """Increment product views."""
        self.views += 1
        self.save(update_fields=['views'])

    def mark_as_sold(self):
        """Mark product as sold."""
        self.is_sold = True
        self.is_active = False
        self.save(update_fields=['is_sold', 'is_active'])


class ProductImage(BaseModel):
    """
    Product image model.
    """
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='images'
    )
    image = models.ImageField(upload_to=generate_product_image_path)
    alt_text = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'product_images'
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"Image for {self.product.title}"


class ProductLike(BaseModel):
    """
    Product like/favorite model.
    """
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='product_likes'
    )
    user = models.ForeignKey(
        'accounts.User', 
        on_delete=models.CASCADE, 
        related_name='liked_products'
    )

    class Meta:
        db_table = 'product_likes'
        verbose_name = 'Product Like'
        verbose_name_plural = 'Product Likes'
        unique_together = ('product', 'user')

    def __str__(self):
        return f"{self.user.display_name} likes {self.product.title}"