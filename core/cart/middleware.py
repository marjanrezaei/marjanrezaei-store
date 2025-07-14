from datetime import timedelta
from django.utils import timezone
from .models import CartModel


class CartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Clean up expired anonymous carts (older than 60 minutes)
        CartModel.objects.filter(
            user__isnull=True,
            created_at__lt=timezone.now() - timedelta(minutes=60)
        ).delete()

        cart = None

        if request.user.is_authenticated:
            cart, _ = CartModel.objects.get_or_create(user=request.user)
        elif request.session.session_key:
            cart = CartModel.objects.filter(session_key=request.session.session_key, user__isnull=True).first()
            if cart:
                request.session['anonymous_cart_session_key'] = request.session.session_key

        if cart:
            request.cart = cart

        return self.get_response(request)
