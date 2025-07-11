"""
Views for chat app.
"""
from rest_framework import generics, permissions
from django.db.models import Q
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationListCreateView(generics.ListCreateAPIView):
    """
    List conversations or create a new conversation.
    """
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(
            participants=self.request.user,
            is_active=True
        ).distinct()


class ConversationDetailView(generics.RetrieveAPIView):
    """
    Get conversation details.
    """
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(
            participants=self.request.user,
            is_active=True
        )


class MessageListCreateView(generics.ListCreateAPIView):
    """
    List messages in a conversation or create a new message.
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        conversation_id = self.kwargs['conversation_id']
        return Message.objects.filter(
            conversation_id=conversation_id,
            conversation__participants=self.request.user
        ).order_by('-created_at')

    def perform_create(self, serializer):
        conversation_id = self.kwargs['conversation_id']
        serializer.save(
            sender=self.request.user,
            conversation_id=conversation_id
        )