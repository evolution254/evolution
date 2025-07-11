"""
Serializers for notifications app.
"""
from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for notifications.
    """
    sender_name = serializers.CharField(source='sender.display_name', read_only=True)

    class Meta:
        model = Notification
        fields = (
            'id', 'recipient', 'sender', 'sender_name', 'notification_type',
            'title', 'message', 'is_read', 'read_at', 'product', 'conversation',
            'created_at'
        )
        read_only_fields = ('recipient', 'created_at')