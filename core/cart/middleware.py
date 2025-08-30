from django.utils.deprecation import MiddlewareMixin
from cart.models import CartModel
from .cart import CartDB

class CartMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # Make sure the session has a key
        if not request.session.session_key:
            request.session.create()

        # Set a key for anonymous users if it doesn't exist yet
        if not request.session.get('anonymous_cart_session_key'):
            request.session['anonymous_cart_session_key'] = request.session.session_key
            request.session.modified = True

        # Attach the cart to the request if not already set
        if getattr(request, 'cart', None):
            return  # Cart already attached

        if request.user.is_authenticated:
            cart, _ = CartModel.objects.get_or_create(user=request.user)
        else:
            session_key = request.session['anonymous_cart_session_key']
            cart, _ = CartModel.objects.get_or_create(session_key=session_key, user__isnull=True)

        request.cart = cart
