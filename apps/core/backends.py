"""
Custom backends for New Revolution.
"""
import resend
from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings
from django.core.mail import EmailMessage
import logging

logger = logging.getLogger(__name__)


class ResendEmailBackend(BaseEmailBackend):
    """
    Email backend using Resend service.
    """
    
    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently, **kwargs)
        self.api_key = getattr(settings, 'RESEND_API_KEY', '')
        if self.api_key:
            resend.api_key = self.api_key

    def send_messages(self, email_messages):
        """
        Send email messages using Resend.
        """
        if not self.api_key:
            logger.error("Resend API key not configured")
            if not self.fail_silently:
                raise ValueError("Resend API key not configured")
            return 0

        sent_count = 0
        
        for message in email_messages:
            try:
                # Prepare email data for Resend
                email_data = {
                    "from": message.from_email or settings.DEFAULT_FROM_EMAIL,
                    "to": message.to,
                    "subject": message.subject,
                }
                
                # Handle HTML and text content
                if hasattr(message, 'alternatives') and message.alternatives:
                    for content, content_type in message.alternatives:
                        if content_type == 'text/html':
                            email_data["html"] = content
                            break
                    email_data["text"] = message.body
                else:
                    email_data["text"] = message.body
                
                # Add CC and BCC if present
                if message.cc:
                    email_data["cc"] = message.cc
                if message.bcc:
                    email_data["bcc"] = message.bcc
                
                # Add reply-to if present
                if message.reply_to:
                    email_data["reply_to"] = message.reply_to
                
                # Send email
                response = resend.Emails.send(email_data)
                
                if response.get('id'):
                    sent_count += 1
                    logger.info(f"Email sent successfully: {response['id']}")
                else:
                    logger.error(f"Failed to send email: {response}")
                    if not self.fail_silently:
                        raise Exception(f"Failed to send email: {response}")
                        
            except Exception as e:
                logger.error(f"Error sending email: {str(e)}")
                if not self.fail_silently:
                    raise e
        
        return sent_count