"""
Utility functions for New Revolution.
"""
import uuid
import os
from django.utils.text import slugify
from django.core.files.storage import default_storage
from PIL import Image
import io


def generate_unique_filename(instance, filename):
    """
    Generate a unique filename for uploaded files.
    """
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return filename


def generate_product_image_path(instance, filename):
    """
    Generate upload path for product images.
    """
    filename = generate_unique_filename(instance, filename)
    return f"products/{instance.product.id}/images/{filename}"


def generate_user_avatar_path(instance, filename):
    """
    Generate upload path for user avatars.
    """
    filename = generate_unique_filename(instance, filename)
    return f"users/{instance.id}/avatar/{filename}"


def create_slug(text, max_length=50):
    """
    Create a URL-friendly slug from text.
    """
    slug = slugify(text)
    if len(slug) > max_length:
        slug = slug[:max_length].rstrip('-')
    return slug


def resize_image(image_file, max_width=1200, max_height=1200, quality=85):
    """
    Resize an image while maintaining aspect ratio.
    """
    try:
        image = Image.open(image_file)
        
        # Convert to RGB if necessary
        if image.mode in ('RGBA', 'LA', 'P'):
            image = image.convert('RGB')
        
        # Calculate new dimensions
        width, height = image.size
        ratio = min(max_width / width, max_height / height)
        
        if ratio < 1:
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Save to bytes
        output = io.BytesIO()
        image.save(output, format='JPEG', quality=quality, optimize=True)
        output.seek(0)
        
        return output
    except Exception as e:
        # Return original file if resize fails
        return image_file


def validate_image_file(file):
    """
    Validate uploaded image file.
    """
    # Check file size (max 10MB)
    if file.size > 10 * 1024 * 1024:
        raise ValueError("File size too large. Maximum size is 10MB.")
    
    # Check file type
    allowed_types = ['image/jpeg', 'image/png', 'image/webp', 'image/gif']
    if file.content_type not in allowed_types:
        raise ValueError("Invalid file type. Only JPEG, PNG, WebP, and GIF are allowed.")
    
    # Validate image
    try:
        image = Image.open(file)
        image.verify()
    except Exception:
        raise ValueError("Invalid image file.")
    
    return True


def send_notification_email(user, subject, template, context=None):
    """
    Send notification email to user.
    """
    from django.core.mail import send_mail
    from django.template.loader import render_to_string
    from django.conf import settings
    
    if context is None:
        context = {}
    
    context.update({
        'user': user,
        'site_name': 'New Revolution',
        'site_url': settings.FRONTEND_DOMAIN or 'https://newrevolution.netlify.app',
    })
    
    html_message = render_to_string(f'emails/{template}.html', context)
    text_message = render_to_string(f'emails/{template}.txt', context)
    
    try:
        send_mail(
            subject=subject,
            message=text_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        # Log error
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Failed to send email to {user.email}: {str(e)}")
        return False


def format_currency(amount, currency='USD'):
    """
    Format currency amount.
    """
    if currency == 'USD':
        return f"${amount:,.2f}"
    return f"{amount:,.2f} {currency}"


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two coordinates in kilometers.
    """
    from math import radians, cos, sin, asin, sqrt
    
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers
    
    return c * r


def generate_verification_code():
    """
    Generate a 6-digit verification code.
    """
    import random
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])


def mask_email(email):
    """
    Mask email address for privacy.
    """
    if '@' not in email:
        return email
    
    username, domain = email.split('@')
    if len(username) <= 2:
        masked_username = username
    else:
        masked_username = username[0] + '*' * (len(username) - 2) + username[-1]
    
    return f"{masked_username}@{domain}"


def mask_phone(phone):
    """
    Mask phone number for privacy.
    """
    if len(phone) <= 4:
        return phone
    
    return phone[:2] + '*' * (len(phone) - 4) + phone[-2:]