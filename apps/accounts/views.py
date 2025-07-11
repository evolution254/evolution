"""
Views for the accounts app.
"""
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from .models import User, UserActivity
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer,
    UserProfileDetailSerializer, PasswordChangeSerializer, EmailVerificationSerializer,
    PhoneVerificationSerializer, UserActivitySerializer, PublicUserSerializer
)
from apps.core.utils import generate_verification_code, send_notification_email
import logging

logger = logging.getLogger(__name__)


class UserRegistrationView(generics.CreateAPIView):
    """
    User registration endpoint.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    @method_decorator(ratelimit(key='ip', rate='5/m', method='POST'))
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == status.HTTP_201_CREATED:
            user = User.objects.get(email=request.data['email'])
            
            # Log registration activity
            UserActivity.objects.create(
                user=user,
                activity_type='registration',
                description='User registered',
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
            )
            
            logger.info(f"New user registered: {user.email}")
            
            return Response({
                'message': 'Registration successful. Please check your email for verification.',
                'user_id': user.id,
                'email': user.email
            }, status=status.HTTP_201_CREATED)
        
        return response


class UserLoginView(TokenObtainPairView):
    """
    User login endpoint with JWT tokens.
    """
    permission_classes = [permissions.AllowAny]

    @method_decorator(ratelimit(key='ip', rate='10/m', method='POST'))
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            
            # Update last active
            user.last_active = timezone.now()
            user.save(update_fields=['last_active'])
            
            # Log login activity
            UserActivity.objects.create(
                user=user,
                activity_type='login',
                description='User logged in',
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
            )
            
            logger.info(f"User logged in: {user.email}")
            
            return Response({
                'access': str(access_token),
                'refresh': str(refresh),
                'user': UserProfileSerializer(user).data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(generics.GenericAPIView):
    """
    User logout endpoint.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            # Log logout activity
            UserActivity.objects.create(
                user=request.user,
                activity_type='logout',
                description='User logged out',
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
            )
            
            logger.info(f"User logged out: {request.user.email}")
            
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Logout error for {request.user.email}: {str(e)}")
            return Response({'error': 'Logout failed'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    User profile view and update endpoint.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        
        if response.status_code == status.HTTP_200_OK:
            # Log profile update activity
            UserActivity.objects.create(
                user=request.user,
                activity_type='profile_update',
                description='User updated profile',
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
            )
            
            logger.info(f"Profile updated: {request.user.email}")
        
        return response


class UserProfileDetailView(generics.RetrieveAPIView):
    """
    Detailed user profile view.
    """
    serializer_class = UserProfileDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class PublicUserProfileView(generics.RetrieveAPIView):
    """
    Public user profile view (for viewing other users).
    """
    queryset = User.objects.filter(is_active=True)
    serializer_class = PublicUserSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'


class PasswordChangeView(generics.GenericAPIView):
    """
    Password change endpoint.
    """
    serializer_class = PasswordChangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @method_decorator(ratelimit(key='user', rate='3/m', method='POST'))
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            # Log password change activity
            UserActivity.objects.create(
                user=request.user,
                activity_type='password_change',
                description='User changed password',
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
            )
            
            logger.info(f"Password changed: {request.user.email}")
            
            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@ratelimit(key='ip', rate='5/m', method='POST')
def verify_email(request):
    """
    Email verification endpoint.
    """
    serializer = EmailVerificationSerializer(data=request.data)
    
    if serializer.is_valid():
        token = serializer.validated_data['token']
        
        try:
            user = User.objects.get(email_verification_token=token)
            user.verify_email()
            
            # Log email verification activity
            UserActivity.objects.create(
                user=user,
                activity_type='email_verification',
                description='User verified email',
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
            )
            
            logger.info(f"Email verified: {user.email}")
            
            return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Invalid verification token'}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@ratelimit(key='user', rate='3/m', method='POST')
def send_phone_verification(request):
    """
    Send phone verification code.
    """
    serializer = PhoneVerificationSerializer(data=request.data)
    
    if serializer.is_valid():
        phone_number = serializer.validated_data['phone_number']
        
        # Generate verification code
        verification_code = generate_verification_code()
        
        # Update user's phone number and verification code
        user = request.user
        user.phone_number = phone_number
        user.phone_verification_code = verification_code
        user.save()
        
        # In a real app, you would send SMS here
        # For demo purposes, we'll just log it
        logger.info(f"Phone verification code for {user.email}: {verification_code}")
        
        return Response({
            'message': 'Verification code sent to your phone',
            'code': verification_code  # Remove this in production
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@ratelimit(key='user', rate='5/m', method='POST')
def verify_phone(request):
    """
    Verify phone number with code.
    """
    serializer = PhoneVerificationSerializer(data=request.data)
    
    if serializer.is_valid():
        verification_code = serializer.validated_data.get('verification_code')
        
        user = request.user
        
        if user.phone_verification_code == verification_code:
            user.verify_phone()
            
            # Log phone verification activity
            UserActivity.objects.create(
                user=user,
                activity_type='phone_verification',
                description='User verified phone number',
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
            )
            
            logger.info(f"Phone verified: {user.email}")
            
            return Response({'message': 'Phone number verified successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserActivityListView(generics.ListAPIView):
    """
    List user activities.
    """
    serializer_class = UserActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserActivity.objects.filter(user=self.request.user).order_by('-created_at')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def become_seller(request):
    """
    Endpoint for users to become sellers.
    """
    user = request.user
    
    if user.is_seller:
        return Response({'error': 'You are already a seller'}, status=status.HTTP_400_BAD_REQUEST)
    
    if not user.is_verified:
        return Response({'error': 'Please verify your email first'}, status=status.HTTP_400_BAD_REQUEST)
    
    user.is_seller = True
    user.save()
    
    # Log seller registration activity
    UserActivity.objects.create(
        user=user,
        activity_type='become_seller',
        description='User became a seller',
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
    )
    
    # Send welcome email
    send_notification_email(
        user=user,
        subject='Welcome to New Revolution Sellers!',
        template='seller_welcome',
    )
    
    logger.info(f"User became seller: {user.email}")
    
    return Response({
        'message': 'Congratulations! You are now a seller.',
        'user': UserProfileSerializer(user).data
    }, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_account(request):
    """
    Delete user account.
    """
    user = request.user
    
    # Log account deletion activity
    UserActivity.objects.create(
        user=user,
        activity_type='account_deletion',
        description='User deleted account',
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
    )
    
    logger.info(f"Account deleted: {user.email}")
    
    # Soft delete - deactivate account
    user.is_active = False
    user.email = f"deleted_{user.id}@deleted.com"
    user.save()
    
    return Response({'message': 'Account deleted successfully'}, status=status.HTTP_200_OK)