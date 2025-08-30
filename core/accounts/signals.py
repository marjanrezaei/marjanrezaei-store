from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from cart.models import CartModel, CartItemModel


@receiver(user_logged_in)
def merge_anonymous_cart(sender, user, request, **kwargs):
    session_key = request.session.get('anonymous_cart_session_key')
    if not session_key:
        return

    anonymous_cart = CartModel.objects.filter(session_key=session_key, user__isnull=True).first()
    if not anonymous_cart:
        return

    user_cart, _ = CartModel.objects.get_or_create(user=user)

    # Merge items from the anonymous cart into the user cart
    for item in anonymous_cart.items.all():
        user_item, created = CartItemModel.objects.get_or_create(
            cart=user_cart,
            product=item.product,
            defaults={'quantity': item.quantity}
        )
        if not created:
            user_item.quantity += item.quantity
            user_item.save(update_fields=['quantity'])

    # Delete the old anonymous cart
    anonymous_cart.delete()

    # Remove the anonymous cart session key
    request.session.pop('anonymous_cart_session_key', None)
    request.session.modified = True

    # Attach the merged cart to the request
    request.cart = user_cart
