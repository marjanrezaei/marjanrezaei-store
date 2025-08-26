from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone
from cart.models import CartModel, CartItemModel

@receiver(user_logged_in)
def merge_anonymous_cart(sender, user, request, **kwargs):
    session_key = request.session.get('anonymous_cart_session_key')
    if not session_key:
        return

    anonymous_cart = CartModel.objects.filter(session_key=session_key, user__isnull=True).first()
    if not anonymous_cart:
        return

    user_cart, created = CartModel.objects.get_or_create(user=user)

    if not created:
        # انتقال آیتم‌ها از anonymous_cart به user_cart
        for item in CartItemModel.objects.filter(cart=anonymous_cart):
            user_item, created = CartItemModel.objects.get_or_create(
                cart=user_cart,
                product=item.product,
                defaults={'quantity': item.quantity}
            )
            if not created:
                user_item.quantity += item.quantity
                user_item.save(update_fields=['quantity'])
        anonymous_cart.delete()
    else:
        # اگر cart کاربر تازه ساخته شد، فقط مالکیت را منتقل کن
        anonymous_cart.user = user
        anonymous_cart.session_key = None
        anonymous_cart.save()
        user_cart = anonymous_cart

    request.cart = user_cart
    del request.session['anonymous_cart_session_key']
    request.session.modified = True
