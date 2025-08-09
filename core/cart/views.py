from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.core.exceptions import ValidationError

from shop.models import ProductModel
from .cart import CartDB
from .models import CartModel
from .mixins import EnsureCartMixin


class CartActionView(View):

    def dispatch(self, request, *args, **kwargs):
        self.ensure_cart(request)
        self.cart = CartDB(request.cart)
        return super().dispatch(request, *args, **kwargs)

    def ensure_cart(self, request):
        if request.user.is_authenticated:
            cart, _ = CartModel.objects.get_or_create(user=request.user)
        else:
            if not request.session.session_key:
                request.session.create()
            session_key = request.session.session_key
            cart, _ = CartModel.objects.get_or_create(session_key=session_key, user__isnull=True)
            request.session['anonymous_cart_session_key'] = session_key
        request.cart = cart

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get("product_id")
        quantity = request.POST.get("quantity")

        if not product_id:
            return JsonResponse({"error": "شناسه محصول الزامی است."}, status=400)

        try:
            self.perform_action(product_id, quantity)
        except ProductModel.DoesNotExist:
            return JsonResponse({"error": "محصول یافت نشد."}, status=404)
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"خطا: {str(e)}"}, status=400)

        return JsonResponse({
            "total_quantity": self.cart.total_quantity,
            "cart_items": self.cart.serialize_items(),
        })

    def perform_action(self, product_id, quantity):
        raise NotImplementedError("Subclasses must implement this method.")


class AddToCartView(CartActionView):
    def perform_action(self, product_id, quantity=None):
        product = get_object_or_404(ProductModel, id=product_id)
        self.cart.add_product(product.id, quantity)


class RemoveProductView(CartActionView):
    def perform_action(self, product_id, quantity):
        self.cart.remove_product(product_id)


class UpdateProductQuantityView(CartActionView):
    def perform_action(self, product_id, quantity):
        if quantity is None:
            raise ValidationError("تعداد محصول الزامی است.")
        qty = int(quantity)
        self.cart.update_product_quantity(product_id, qty)
        

class CartSummaryView(EnsureCartMixin, TemplateView):
    template_name = "cart/cart-summary.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.get_cart()
        cart_items = cart.get_cart_items()

        for item in cart_items:
            item['quantity_range'] = range(1, item['product_obj'].stock + 1)
    
        context.update({
            "cart_items": cart_items,
            "total_quantity": cart.total_quantity,
            "total_payment_price": cart.get_total_payment_amount(),
        })
        return context




