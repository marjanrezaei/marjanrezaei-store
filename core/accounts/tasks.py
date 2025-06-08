from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse

from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def send_reset_email(email):
    
    user = User.objects.get(email=email)  # Get user object
    token = default_token_generator.make_token(user)  # Generate token
    uid = urlsafe_base64_encode(force_bytes(user.pk))  # Encode user ID
    reset_url = f"http://127.0.0.1:8080{reverse('acconts:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})}"
            
    send_mail(reset_url, "noreply@yourdomain.com", [email])


