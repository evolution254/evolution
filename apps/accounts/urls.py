"""
URL configuration for accounts app.
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Profile
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/detail/', views.UserProfileDetailView.as_view(), name='profile_detail'),
    path('profile/<uuid:id>/', views.PublicUserProfileView.as_view(), name='public_profile'),
    
    # Password
    path('password/change/', views.PasswordChangeView.as_view(), name='password_change'),
    
    # Verification
    path('verify/email/', views.verify_email, name='verify_email'),
    path('verify/phone/send/', views.send_phone_verification, name='send_phone_verification'),
    path('verify/phone/', views.verify_phone, name='verify_phone'),
    
    # Activities
    path('activities/', views.UserActivityListView.as_view(), name='activities'),
    
    # Seller
    path('become-seller/', views.become_seller, name='become_seller'),
    
    # Account management
    path('delete/', views.delete_account, name='delete_account'),
]