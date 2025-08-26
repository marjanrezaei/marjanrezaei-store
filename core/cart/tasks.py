from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import CartModel

@shared_task
def cleanup_old_carts():
    cutoff = timezone.now() - timedelta(hours=1)
    CartModel.objects.filter(user__isnull=True, created_at__lt=cutoff).delete()
