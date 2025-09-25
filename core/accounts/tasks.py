from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse
from datetime import datetime, timedelta
import jwt
from .models import User

@shared_task
def send_reset_email(email):
    try:
        # Try to get the user by email
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # Return if the user does not exist
        return "User not found"

    # Create JWT for password reset
    payload = {
        "user_id": user.id,
        "type": "password_reset",
        "exp": datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    # Determine domain based on environment (development or production)
    domain = 'http://127.0.0.1:8000' if settings.DEBUG else 'https://marjanrezaei-store.onrender.com'

    # Get API path for password reset confirmation
    path = reverse('accounts_api:password-reset-confirm-api')
    reset_link = f"{domain}{path}?token={token}"

    # Render the email template with user and reset link
    message = render_to_string("accounts/password_reset_email.html", {
        "user": user,
        "reset_link": reset_link,
    })

    # Create email message
    email_message = EmailMessage(
        subject="Password Reset Request",
        body=message,
        to=[email],
        from_email=settings.DEFAULT_FROM_EMAIL,
    )
    email_message.content_subtype = "html"  # Send as HTML email
    email_message.send()

    # Print success messages for logging/debugging
    print(f"[SUCCESS] Password reset email sent to {email}")
    print(f"Reset link: {reset_link}")
    return "Reset email sent"
