from django.utils import timezone

class CartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # مطمئن شدن session key ساخته شده
        if not request.session.session_key:
            request.session.save()

        # ست کردن session key برای cart ناشناس
        request.session['anonymous_cart_session_key'] = request.session.session_key
        request.session.modified = True

        # cart را روی request قرار می‌دهد (بعد از login merge خواهد شد)
        request.cart = None
        return self.get_response(request)
