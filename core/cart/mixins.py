from .models import CartModel
from .cart import CartDB

class EnsureCartMixin:
    def get_cart(self):
        request = self.request

        if hasattr(request, 'cart') and request.cart:
            return CartDB(request.cart)

        if request.user.is_authenticated:
            cart, _ = CartModel.objects.get_or_create(user=request.user)
        else:
            if not request.session.session_key:
                request.session.create()
            session_key = request.session.session_key
            cart, _ = CartModel.objects.get_or_create(session_key=session_key, user__isnull=True)
            request.session['anonymous_cart_session_key'] = session_key

        request.cart = cart
        return CartDB(cart)
