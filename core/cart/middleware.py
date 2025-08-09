from datetime import timedelta
from django.utils import timezone
from django.db import connection
from .models import CartModel

def table_exists(table_name):
    return table_name in connection.introspection.table_names()

class CartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if table_exists('cart_cartmodel'):
            # اطمینان از اینکه session ساخته شده
            if not request.session.session_key:
                request.session.save()

            # پاک‌سازی سبدهای خرید ناشناس قدیمی
            CartModel.objects.filter(
                user__isnull=True,
                created_at__lt=timezone.now() - timedelta(minutes=60)
            ).delete()

            cart = None

            if request.user.is_authenticated:
                # انتقال سبد خرید ناشناس به حساب کاربری
                old_session_key = request.session.get('anonymous_cart_session_key')
                if old_session_key:
                    anonymous_cart = CartModel.objects.filter(
                        session_key=old_session_key,
                        user__isnull=True
                    ).first()
                    if anonymous_cart:
                        anonymous_cart.user = request.user
                        anonymous_cart.session_key = None
                        anonymous_cart.save()
                        cart = anonymous_cart
                        del request.session['anonymous_cart_session_key']
                        request.session.modified = True

                # گرفتن یا ساختن سبد خرید کاربر
                if not cart:
                    cart, _ = CartModel.objects.get_or_create(user=request.user)

            else:
                # کاربر ناشناس
                cart = CartModel.objects.filter(
                    session_key=request.session.session_key,
                    user__isnull=True
                ).first()

                if not cart:
                    cart = CartModel.objects.create(session_key=request.session.session_key)

                request.session['anonymous_cart_session_key'] = request.session.session_key
                request.session.modified = True

            # اتصال سبد خرید به request
            request.cart = cart

        return self.get_response(request)