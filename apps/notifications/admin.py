"""
Admin configuration for notifications app.
"""
from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'recipient', 'sender', 'notification_type', 'title',
        'is_read', 'created_at'
    )
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('recipient__email', 'sender__email', 'title', 'message')
    readonly_fields = ('created_at', 'updated_at', 'read_at')