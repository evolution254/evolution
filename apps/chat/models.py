"""
Chat models for New Revolution marketplace.
"""
from django.db import models
from apps.core.models import BaseModel


class Conversation(BaseModel):
    """
    Conversation between users.
    """
    participants = models.ManyToManyField(
        'accounts.User',
        related_name='conversations'
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='conversations',
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'conversations'
        verbose_name = 'Conversation'
        verbose_name_plural = 'Conversations'
        ordering = ['-updated_at']

    def __str__(self):
        participants = ", ".join([user.display_name for user in self.participants.all()])
        return f"Conversation: {participants}"

    @property
    def last_message(self):
        """Get the last message in this conversation."""
        return self.messages.first()


class Message(BaseModel):
    """
    Message in a conversation.
    """
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'messages'
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.sender.display_name}: {self.content[:50]}"