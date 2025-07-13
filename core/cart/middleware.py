from datetime import timedelta
from django.utils import timezone
from .models import CartModel

class CartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Clean up expired anonymous carts (older than 60 minute)
        CartModel.objects.filter(
            user__isnull=True,
            created_at__lt=timezone.now() - timedelta(minutes=60)
        ).delete()

        # Handle session key
        session_key = request.session.session_key
        if not session_key and not request.user.is_authenticated:
            request.session.create()
            session_key = request.session.session_key

        # Get or create cart
        if request.user.is_authenticated:
            cart, _ = CartModel.objects.get_or_create(user=request.user)
        else:
            cart = None
            if session_key:
                cart, _ = CartModel.objects.get_or_create(session_key=session_key, user__isnull=True)
                request.session['anonymous_cart_session_key'] = session_key

        request.cart = cart
        return self.get_response(request)
