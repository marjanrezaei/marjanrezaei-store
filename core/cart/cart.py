from shop.models import ProductStatusType
from django.db.models import Sum, F
from .models import CartItemModel

class CartDB:
    def __init__(self, cart_model_instance):
        self.cart = cart_model_instance

    def add_product(self, product_id):
        product_id = int(product_id)
        cart_item, created = CartItemModel.objects.get_or_create(
            cart=self.cart,
            product_id=product_id,
            defaults={"quantity": 1}
        )
        if not created:
            cart_item.quantity = F('quantity') + 1
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
        else:
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

    def get_cart_items(self):
        cart_items = CartItemModel.objects.filter(cart=self.cart).select_related('product')
        items = []
        for item in cart_items:
            product = item.product
            if product.status != ProductStatusType.publish.value:
                continue
            total_price = item.quantity * product.get_price()
            items.append({
                "product_obj": product,
                "quantity": item.quantity,
                "total_price": total_price,
            })
        return items

    def get_total_payment_amount(self):
        return sum(item["total_price"] for item in self.get_cart_items())

    def serialize_items(self):
        cart_items = CartItemModel.objects.filter(cart=self.cart).select_related('product')
        serialized = []
        for item in cart_items:
            product = item.product
            if product.status != ProductStatusType.publish.value:
                continue
            serialized.append({
                "product_id": product.id,
                "product_name": product.title,
                "quantity": item.quantity,
                "unit_price": product.get_price(),
                "total_price": item.quantity * product.get_price(),
            })
        return serialized
