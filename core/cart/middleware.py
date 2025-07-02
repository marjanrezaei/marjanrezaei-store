from .models import CartModel

class CartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Ensure the session has a key
        if not request.session.session_key:
            request.session.create()

        session_key = request.session.session_key

        if request.user.is_authenticated:
            # Retrieve or create cart associated with logged-in user
            cart, _ = CartModel.objects.get_or_create(user=request.user)
        else:
            # Retrieve or create cart associated with anonymous session
            cart, _ = CartModel.objects.get_or_create(session_key=session_key, user__isnull=True)

            # Save the session_key of anonymous cart for later merging after login
            request.session['anonymous_cart_session_key'] = session_key

        # Attach the cart instance to the request object for easy access in views
        request.cart = cart

        response = self.get_response(request)
        return response
