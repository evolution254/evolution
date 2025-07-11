"""
Serializers for chat app.
"""
from rest_framework import serializers
from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for messages.
    """
    sender_name = serializers.CharField(source='sender.display_name', read_only=True)

    class Meta:
        model = Message
        fields = (
            'id', 'conversation', 'sender', 'sender_name', 'content',
            'is_read', 'read_at', 'created_at'
        )
        read_only_fields = ('sender', 'created_at')


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for conversations.
    """
    last_message = MessageSerializer(read_only=True)
    participants_names = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = (
            'id', 'participants', 'participants_names', 'product',
            'is_active', 'last_message', 'created_at', 'updated_at'
        )

    def get_participants_names(self, obj):
        return [user.display_name for user in obj.participants.all()]