from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import CartModel, CartItemModel

@receiver(user_logged_in)
def merge_session_cart_to_db(sender, request, user, **kwargs):
    old_session_key = request.session.get('anonymous_cart_session_key')

    if not old_session_key:
        return

    try:
        session_cart = CartModel.objects.get(session_key=old_session_key)
    except CartModel.DoesNotExist:
        return

    user_cart, _ = CartModel.objects.get_or_create(user=user)

    session_items = CartItemModel.objects.filter(cart=session_cart)
    for item in session_items:
        user_item, created = CartItemModel.objects.get_or_create(
            cart=user_cart,
            product=item.product,
            defaults={'quantity': item.quantity}
        )
        if not created:
            user_item.quantity += item.quantity
            user_item.save(update_fields=['quantity'])

    session_cart.delete()

    request.session.pop('anonymous_cart_session_key', None)
    request.session.modified = True
