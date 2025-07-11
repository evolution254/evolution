"""
Serializers for the accounts app.
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User, UserProfile, UserActivity
from apps.core.utils import generate_verification_code, send_notification_email
import uuid


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password', 'password_confirm')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        
        # Generate email verification token
        user.email_verification_token = str(uuid.uuid4())
        user.save()
        
        # Send verification email
        send_notification_email(
            user=user,
            subject='Welcome to New Revolution - Verify Your Email',
            template='welcome_verification',
            context={'verification_token': user.email_verification_token}
        )
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            
            if not user:
                raise serializers.ValidationError('Invalid email or password.')
            
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
            
            if user.is_banned:
                raise serializers.ValidationError('Your account has been banned.')
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Must include email and password.')


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile.
    """
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    display_name = serializers.CharField(read_only=True)
    is_active_seller = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name', 'full_name', 'display_name',
            'phone_number', 'avatar', 'bio', 'location', 'is_verified', 'is_phone_verified',
            'is_seller', 'is_active_seller', 'seller_rating', 'total_sales',
            'email_notifications', 'sms_notifications', 'marketing_emails',
            'created_at', 'last_active'
        )
        read_only_fields = (
            'id', 'email', 'is_verified', 'is_phone_verified', 'seller_rating', 
            'total_sales', 'created_at', 'last_active'
        )

    def update(self, instance, validated_data):
        # Handle avatar upload
        if 'avatar' in validated_data:
            avatar = validated_data['avatar']
            if avatar:
                # Validate and resize image
                from apps.core.utils import validate_image_file, resize_image
                validate_image_file(avatar)
                resized_avatar = resize_image(avatar, max_width=400, max_height=400)
                validated_data['avatar'] = resized_avatar

        return super().update(instance, validated_data)


class UserProfileDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for user profile with extended information.
    """
    profile = serializers.SerializerMethodField()
    stats = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name', 'phone_number',
            'avatar', 'bio', 'location', 'is_verified', 'is_phone_verified',
            'is_seller', 'seller_rating', 'total_sales', 'created_at', 'profile', 'stats'
        )

    def get_profile(self, obj):
        try:
            profile = obj.profile
            return {
                'date_of_birth': profile.date_of_birth,
                'gender': profile.gender,
                'website': profile.website,
                'business_name': profile.business_name,
                'business_type': profile.business_type,
                'preferred_language': profile.preferred_language,
                'preferred_currency': profile.preferred_currency,
            }
        except UserProfile.DoesNotExist:
            return None

    def get_stats(self, obj):
        from apps.products.models import Product
        from apps.reviews.models import Review
        
        return {
            'total_products': Product.objects.filter(seller=obj, is_active=True).count(),
            'total_reviews': Review.objects.filter(product__seller=obj).count(),
            'followers_count': obj.followers.count(),
            'following_count': obj.following.count(),
        }


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for password change.
    """
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect.')
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match.")
        return attrs

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class EmailVerificationSerializer(serializers.Serializer):
    """
    Serializer for email verification.
    """
    token = serializers.CharField()

    def validate_token(self, value):
        try:
            user = User.objects.get(email_verification_token=value)
            if user.is_verified:
                raise serializers.ValidationError('Email is already verified.')
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid verification token.')


class PhoneVerificationSerializer(serializers.Serializer):
    """
    Serializer for phone verification.
    """
    phone_number = serializers.CharField()
    verification_code = serializers.CharField(max_length=6, required=False)

    def validate_phone_number(self, value):
        # Basic phone number validation
        import re
        if not re.match(r'^\+?1?\d{9,15}$', value):
            raise serializers.ValidationError('Invalid phone number format.')
        return value


class UserActivitySerializer(serializers.ModelSerializer):
    """
    Serializer for user activities.
    """
    class Meta:
        model = UserActivity
        fields = ('id', 'activity_type', 'description', 'created_at', 'metadata')
        read_only_fields = ('id', 'created_at')


class PublicUserSerializer(serializers.ModelSerializer):
    """
    Public serializer for user information (for other users to see).
    """
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    display_name = serializers.CharField(read_only=True)
    stats = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name', 'full_name', 'display_name',
            'avatar', 'bio', 'location', 'is_verified', 'is_seller', 'seller_rating',
            'total_sales', 'created_at', 'stats'
        )

    def get_stats(self, obj):
        from apps.products.models import Product
        from apps.reviews.models import Review
        
        return {
            'total_products': Product.objects.filter(seller=obj, is_active=True).count(),
            'average_rating': obj.seller_rating,
            'total_reviews': Review.objects.filter(product__seller=obj).count(),
            'member_since': obj.created_at.year,
        }