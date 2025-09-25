from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderModel, OrderStatusType
from django.db import transaction
from django.utils.translation import gettext_lazy as _


@receiver(post_save, sender=OrderModel)
def reduce_product_stock_after_order(sender, instance, created, **kwargs):
    """
    Deduct product stock after order is marked as SUCCESS.
    """
    if not created and instance.status == OrderStatusType.SUCCESS:
        order = instance

        # Avoid double deduction
        if hasattr(order, '_stock_already_deducted'):
            return

        with transaction.atomic():
            for item in order.order_items.select_related('product'):
                product = item.product
                if product.stock < item.quantity:
                    raise ValueError(
                        _(f"Not enough stock for product {product.title}.")
                    )
                product.stock -= item.quantity
                product.save()

        order._stock_already_deducted = True
