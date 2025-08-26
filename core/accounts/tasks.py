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
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return "User not found"

    # ایجاد JWT برای ریست پسورد
    payload = {
        "user_id": user.id,
        "type": "password_reset",
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    # تعیین دامنه بر اساس محیط
    domain = 'http://127.0.0.1:8000' if settings.DEBUG else 'https://marjanrezaei-store.onrender.com'

    # مسیر API ریست پسورد
    path = reverse('accounts_api:password-reset-confirm-api')
    reset_link = f"{domain}{path}?token={token}"

    # رندر قالب ایمیل
    message = render_to_string("accounts/password_reset_email.html", {
        "user": user,
        "reset_link": reset_link,
    })

    email_message = EmailMessage(
        subject="Password Reset Request",
        body=message,
        to=[email],
        from_email=settings.DEFAULT_FROM_EMAIL,
    )
    email_message.content_subtype = "html"
    email_message.send()

    print(f"[SUCCESS] Password reset email sent to {email}")
    print(f"Reset link: {reset_link}")
    return "Reset email sent"
