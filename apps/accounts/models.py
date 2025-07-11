"""
User models for New Revolution marketplace.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from apps.core.models import TimeStampedModel
from apps.core.utils import generate_user_avatar_path
import uuid


class User(AbstractUser):
    """
    Custom user model for New Revolution.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )]
    )
    avatar = models.ImageField(upload_to=generate_user_avatar_path, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    
    # Verification fields
    is_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=100, blank=True)
    phone_verification_code = models.CharField(max_length=6, blank=True)
    
    # Account status
    is_banned = models.BooleanField(default=False)
    ban_reason = models.TextField(blank=True)
    banned_until = models.DateTimeField(null=True, blank=True)
    
    # Seller information
    is_seller = models.BooleanField(default=False)
    seller_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_sales = models.PositiveIntegerField(default=0)
    
    # Preferences
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    marketing_emails = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_active = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    def get_full_name(self):
        """Return the full name of the user."""
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    @property
    def display_name(self):
        """Return display name for the user."""
        full_name = self.get_full_name()
        return full_name if full_name else self.username

    @property
    def is_active_seller(self):
        """Check if user is an active seller."""
        return self.is_seller and not self.is_banned and self.is_verified

    def ban_user(self, reason, until=None):
        """Ban the user."""
        self.is_banned = True
        self.ban_reason = reason
        self.banned_until = until
        self.save()

    def unban_user(self):
        """Unban the user."""
        self.is_banned = False
        self.ban_reason = ''
        self.banned_until = None
        self.save()

    def verify_email(self):
        """Mark email as verified."""
        self.is_verified = True
        self.email_verification_token = ''
        self.save()

    def verify_phone(self):
        """Mark phone as verified."""
        self.is_phone_verified = True
        self.phone_verification_code = ''
        self.save()


class UserProfile(TimeStampedModel):
    """
    Extended user profile information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
            ('prefer_not_to_say', 'Prefer not to say'),
        ],
        blank=True
    )
    website = models.URLField(blank=True)
    social_media = models.JSONField(default=dict, blank=True)
    
    # Address information
    address_line_1 = models.CharField(max_length=255, blank=True)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    
    # Business information (for sellers)
    business_name = models.CharField(max_length=255, blank=True)
    business_type = models.CharField(max_length=100, blank=True)
    tax_id = models.CharField(max_length=50, blank=True)
    
    # Preferences
    preferred_language = models.CharField(max_length=10, default='en')
    preferred_currency = models.CharField(max_length=3, default='USD')
    timezone = models.CharField(max_length=50, default='UTC')

    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"Profile of {self.user.display_name}"


class UserActivity(TimeStampedModel):
    """
    Track user activities for analytics and security.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(
        max_length=50,
        choices=[
            ('login', 'Login'),
            ('logout', 'Logout'),
            ('product_view', 'Product View'),
            ('product_create', 'Product Create'),
            ('product_update', 'Product Update'),
            ('product_delete', 'Product Delete'),
            ('message_send', 'Message Send'),
            ('review_create', 'Review Create'),
            ('payment_made', 'Payment Made'),
            ('profile_update', 'Profile Update'),
        ]
    )
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'user_activities'
        verbose_name = 'User Activity'
        verbose_name_plural = 'User Activities'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.display_name} - {self.activity_type} at {self.created_at}"


class UserFollowing(TimeStampedModel):
    """
    User following system.
    """
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    class Meta:
        db_table = 'user_following'
        verbose_name = 'User Following'
        verbose_name_plural = 'User Following'
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.display_name} follows {self.following.display_name}"


class UserBlock(TimeStampedModel):
    """
    User blocking system.
    """
    blocker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocking')
    blocked = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_by')
    reason = models.TextField(blank=True)

    class Meta:
        db_table = 'user_blocks'
        verbose_name = 'User Block'
        verbose_name_plural = 'User Blocks'
        unique_together = ('blocker', 'blocked')

    def __str__(self):
        return f"{self.blocker.display_name} blocked {self.blocked.display_name}"