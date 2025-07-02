from django.db.models import Sum
from .models import CartModel

def cart_total_quantity(request):
    total_quantity = 0

    try:
        if request.user.is_authenticated:
            cart = CartModel.objects.get(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                return {'total_quantity': 0}
            cart = CartModel.objects.get(session_key=session_key, user__isnull=True)
    except CartModel.DoesNotExist:
        return {'total_quantity': 0}

    total_quantity = cart.items.aggregate(total=Sum('quantity'))['total'] or 0


    return {'total_quantity': total_quantity}
