"""
Category models for New Revolution marketplace.
"""
from django.db import models
from apps.core.models import TimeStampedModel
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel, TimeStampedModel):
    """
    Product category model with hierarchical structure.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class MPTTMeta:
        order_insertion_by = ['order', 'name']

    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    @property
    def product_count(self):
        """Get the number of active products in this category."""
        return self.products.filter(is_active=True, is_deleted=False).count()