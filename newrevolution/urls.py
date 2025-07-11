"""
URL configuration for newrevolution project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from apps.core.views import HealthCheckView, APIRootView

# API Router
router = DefaultRouter()

# API URL patterns
api_patterns = [
    path('', APIRootView.as_view(), name='api-root'),
    path('auth/', include('apps.accounts.urls')),
    path('products/', include('apps.products.urls')),
    path('categories/', include('apps.categories.urls')),
    path('reviews/', include('apps.reviews.urls')),
    path('chat/', include('apps.chat.urls')),
    path('payments/', include('apps.payments.urls')),
    path('notifications/', include('apps.notifications.urls')),
]

urlpatterns = [
    # Admin
    path(settings.ADMIN_URL, admin.site.urls),
    
    # Health check
    path('health/', HealthCheckView.as_view(), name='health-check'),
    
    # API
    path('api/v1/', include(api_patterns)),
    
    # Router URLs
    path('api/v1/', include(router.urls)),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom admin configuration
admin.site.site_header = "New Revolution Admin"
admin.site.site_title = "New Revolution Admin Portal"
admin.site.index_title = "Welcome to New Revolution Administration"