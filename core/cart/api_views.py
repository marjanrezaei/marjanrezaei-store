# cart_api.py
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from .serializers import CartItemSerializer
from shop.models import ProductModel
from .cart import CartDB
from .models import CartModel


class CartMixin:
    def ensure_cart(self, request):
        """
        Ensure that request.cart and self.cart are always available.
        """
        if getattr(request, 'cart', None):
            if not getattr(self, 'cart', None):
                self.cart = CartDB(request.cart)
            return

        if request.user.is_authenticated:
            cart, _ = CartModel.objects.get_or_create(user=request.user)
        else:
            if not request.session.session_key:
                request.session.create()
            session_key = request.session.session_key
            cart, _ = CartModel.objects.get_or_create(session_key=session_key, user__isnull=True)
            request.session['anonymous_cart_session_key'] = session_key

        request.cart = cart
        self.cart = CartDB(cart)


class AddToCartAPIView(CartMixin, APIView):
    permission_classes = [AllowAny]

    def post(self, request, product_id):
        self.ensure_cart(request)

        # Quantity
        try:
            quantity = int(request.data.get("quantity", 1))
            if quantity <= 0:
                quantity = 1
        except (ValueError, TypeError):
            quantity = 1

        product = get_object_or_404(ProductModel, id=product_id)

        try:
            self.cart.add_product(product.id, quantity)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "total_quantity": self.cart.total_quantity,
            "cart_items": CartItemSerializer(self.cart.get_items_queryset(), many=True).data
        }, status=status.HTTP_200_OK)


class RemoveProductAPIView(CartMixin, APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        self.ensure_cart(request)
        product_id = request.data.get("product_id")
        if not product_id:
            return Response({"error": "Product ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            self.cart.remove_product(product_id)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "total_quantity": self.cart.total_quantity,
            "cart_items": CartItemSerializer(self.cart.get_items_queryset(), many=True).data
        })


class UpdateProductQuantityAPIView(CartMixin, APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        self.ensure_cart(request)
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity")

        if not product_id:
            return Response({"error": "Product ID is required."}, status=400)
        if quantity is None:
            return Response({"error": "Quantity is required."}, status=400)

        try:
            qty = int(quantity)
            self.cart.update_product_quantity(product_id, qty)
        except ValidationError as e:
            return Response({"error": str(e)}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

        item = self.cart.get_item(product_id)
        item_total = item.quantity * item.product.get_price() if item else 0


        return Response({
            "total_quantity": self.cart.total_quantity,
            "cart_total": self.cart.get_total_payment_amount(),
            "item_total": item_total
        })


class CartSummaryAPIView(CartMixin, APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            self.ensure_cart(request)

            cart_items_qs = self.cart.get_items_queryset()
            serializer = CartItemSerializer(cart_items_qs, many=True)

            return Response({
                "cart_items": serializer.data,
                "total_quantity": self.cart.total_quantity,
                "total_payment_price": self.cart.get_total_payment_amount()
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print("Error fetching cart:", e)
            return Response({"error": "Could not fetch cart"}, status=500)
