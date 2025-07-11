"""
Admin configuration for accounts app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, UserProfile, UserActivity, UserFollowing, UserBlock


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin interface for User model.
    """
    list_display = (
        'email', 'username', 'first_name', 'last_name', 'is_verified', 
        'is_seller', 'is_banned', 'is_active', 'created_at'
    )
    list_filter = (
        'is_verified', 'is_seller', 'is_banned', 'is_active', 'is_staff', 
        'is_superuser', 'created_at'
    )
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'avatar', 'bio', 'location')}),
        ('Verification', {'fields': ('is_verified', 'is_phone_verified', 'email_verification_token', 'phone_verification_code')}),
        ('Seller info', {'fields': ('is_seller', 'seller_rating', 'total_sales')}),
        ('Account status', {'fields': ('is_banned', 'ban_reason', 'banned_until')}),
        ('Preferences', {'fields': ('email_notifications', 'sms_notifications', 'marketing_emails')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'last_active')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ('created_at', 'last_active')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('profile')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for UserProfile model.
    """
    list_display = ('user', 'business_name', 'city', 'country', 'preferred_currency')
    list_filter = ('gender', 'country', 'preferred_currency', 'preferred_language')
    search_fields = ('user__email', 'user__username', 'business_name', 'city')
    
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Personal Info', {'fields': ('date_of_birth', 'gender', 'website')}),
        ('Address', {'fields': ('address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country')}),
        ('Business Info', {'fields': ('business_name', 'business_type', 'tax_id')}),
        ('Preferences', {'fields': ('preferred_language', 'preferred_currency', 'timezone')}),
        ('Social Media', {'fields': ('social_media',)}),
    )


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    """
    Admin interface for UserActivity model.
    """
    list_display = ('user', 'activity_type', 'created_at', 'ip_address')
    list_filter = ('activity_type', 'created_at')
    search_fields = ('user__email', 'user__username', 'activity_type', 'description')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(UserFollowing)
class UserFollowingAdmin(admin.ModelAdmin):
    """
    Admin interface for UserFollowing model.
    """
    list_display = ('follower', 'following', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('follower__email', 'following__email')
    readonly_fields = ('created_at',)


@admin.register(UserBlock)
class UserBlockAdmin(admin.ModelAdmin):
    """
    Admin interface for UserBlock model.
    """
    list_display = ('blocker', 'blocked', 'reason', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('blocker__email', 'blocked__email', 'reason')
    readonly_fields = ('created_at',)