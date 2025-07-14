from shop.models import ProductStatusType
from django.db.models import Sum, F
from .models import CartItemModel


class CartDB:
    def __init__(self, cart_model_instance):
        self.cart = cart_model_instance

    def add_product(self, product_id, quantity=1):
        """Add product with optional quantity (default is 1)."""
        product_id = int(product_id)
        quantity = int(quantity) if quantity else 1

        cart_item, created = CartItemModel.objects.get_or_create(
            cart=self.cart,
            product_id=product_id,
            defaults={"quantity": quantity}
        )
        if not created:
            # Use F expression and refresh to avoid race conditions
            cart_item.quantity = F('quantity') + quantity
            cart_item.save(update_fields=['quantity'])
            cart_item.refresh_from_db()

    def remove_product(self, product_id):
        product_id = int(product_id)
        CartItemModel.objects.filter(cart=self.cart, product_id=product_id).delete()

    def update_product_quantity(self, product_id, quantity):
        product_id = int(product_id)
        quantity = int(quantity)

        if quantity <= 0:
            self.remove_product(product_id)
            return

        cart_item, created = CartItemModel.objects.get_or_create(
            cart=self.cart,
            product_id=product_id,
            defaults={"quantity": quantity}
        )
        if not created:
            cart_item.quantity = quantity
            cart_item.save(update_fields=['quantity'])

    def clear(self):
        CartItemModel.objects.filter(cart=self.cart).delete()

    @property
    def total_quantity(self):
        return CartItemModel.objects.filter(cart=self.cart).aggregate(
            total=Sum('quantity')
        )['total'] or 0

    def _serialize_item(self, item):
        product = item.product
        price = product.get_price()
        return {
            "product_id": product.id,
            "product_name": product.title,
            "quantity": item.quantity,
            "unit_price": price,
            "total_price": item.quantity * price,
            "product_obj": product,  # optional for internal logic
        }

    def get_cart_items(self):
        cart_items = CartItemModel.objects.filter(
            cart=self.cart
        ).select_related('product')

        items = []
        for item in cart_items:
            if item.product.status != ProductStatusType.publish.value:
                continue
            items.append(self._serialize_item(item))
        return items

    def get_total_payment_amount(self):
        return sum(item["total_price"] for item in self.get_cart_items())

    def serialize_items(self):
        return [
            {k: v for k, v in item.items() if k != "product_obj"}
            for item in self.get_cart_items()
        ]
