from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderModel, OrderStatusType
from django.db import transaction

@receiver(post_save, sender=OrderModel)
def reduce_product_stock_after_order(sender, instance, created, **kwargs):
    if not created and instance.status == OrderStatusType.SUCCESS:
        order = instance

        # بررسی اینکه آیا قبلاً پردازش شده یا نه (برای جلوگیری از کاهش دوباره)
        if hasattr(order, '_stock_already_deducted'):
            return

        with transaction.atomic():
            for item in order.order_items.select_related('product'):
                product = item.product
                if product.stock < item.quantity:
                    raise ValueError(f"موجودی کافی برای محصول {product.title} وجود ندارد.")
                product.stock -= item.quantity
                product.save()
        
        # پرچم برای جلوگیری از کاهش دوباره
        order._stock_already_deducted = True
