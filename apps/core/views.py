"""
Core views for the New Revolution marketplace.
"""
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import redis
import os


class HealthCheckView(APIView):
    """
    Health check endpoint for monitoring.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        """
        Perform health checks on various services.
        """
        health_status = {
            'status': 'healthy',
            'timestamp': timezone.now().isoformat(),
            'services': {}
        }

        # Check database connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            health_status['services']['database'] = 'healthy'
        except Exception as e:
            health_status['services']['database'] = f'unhealthy: {str(e)}'
            health_status['status'] = 'unhealthy'

        # Check Redis connection
        try:
            cache.set('health_check', 'ok', 10)
            cache.get('health_check')
            health_status['services']['redis'] = 'healthy'
        except Exception as e:
            health_status['services']['redis'] = f'unhealthy: {str(e)}'
            health_status['status'] = 'unhealthy'

        # Check environment variables
        required_env_vars = ['SECRET_KEY', 'DATABASE_URL']
        missing_vars = [var for var in required_env_vars if not os.getenv(var)]
        
        if missing_vars:
            health_status['services']['environment'] = f'missing variables: {", ".join(missing_vars)}'
            health_status['status'] = 'unhealthy'
        else:
            health_status['services']['environment'] = 'healthy'

        response_status = status.HTTP_200_OK if health_status['status'] == 'healthy' else status.HTTP_503_SERVICE_UNAVAILABLE
        
        return Response(health_status, status=response_status)


class APIRootView(APIView):
    """
    API root endpoint with available endpoints.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        """
        Return available API endpoints.
        """
        return Response({
            'message': 'Welcome to New Revolution API',
            'version': 'v1',
            'endpoints': {
                'auth': {
                    'login': '/api/v1/auth/login/',
                    'register': '/api/v1/auth/register/',
                    'logout': '/api/v1/auth/logout/',
                    'profile': '/api/v1/auth/profile/',
                    'refresh': '/api/v1/auth/token/refresh/',
                },
                'products': {
                    'list': '/api/v1/products/',
                    'create': '/api/v1/products/',
                    'detail': '/api/v1/products/{id}/',
                    'my_products': '/api/v1/products/my-products/',
                    'featured': '/api/v1/products/featured/',
                    'trending': '/api/v1/products/trending/',
                },
                'categories': {
                    'list': '/api/v1/categories/',
                    'tree': '/api/v1/categories/tree/',
                },
                'reviews': {
                    'list': '/api/v1/reviews/',
                    'create': '/api/v1/reviews/',
                },
                'chat': {
                    'conversations': '/api/v1/chat/conversations/',
                    'messages': '/api/v1/chat/conversations/{id}/messages/',
                },
                'payments': {
                    'create_intent': '/api/v1/payments/create-intent/',
                    'boost_packages': '/api/v1/payments/boost-packages/',
                },
                'notifications': {
                    'list': '/api/v1/notifications/',
                    'mark_read': '/api/v1/notifications/{id}/mark-read/',
                },
            },
            'documentation': '/api/v1/docs/',
            'health': '/health/',
        })