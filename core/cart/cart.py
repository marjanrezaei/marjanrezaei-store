from django.db.models import F, Sum
from .models import CartItemModel
from shop.models import ProductStatusType

class CartDB:
    def __init__(self, cart_model_instance):
        self.cart = cart_model_instance

    # ---------------------- CRUD METHODS ----------------------
    def add_product(self, product_id, quantity=1):
        product_id = int(product_id)
        quantity = int(quantity) if quantity else 1

        cart_item, created = CartItemModel.objects.get_or_create(
            cart=self.cart,
            product_id=product_id,
            defaults={"quantity": quantity}
        )
        if not created:
            cart_item.quantity = F('quantity') + quantity
            cart_item.save(update_fields=['quantity'])
            cart_item.refresh_from_db()

    def remove_product(self, product_id):
        CartItemModel.objects.filter(cart=self.cart, product_id=product_id).delete()

    def update_product_quantity(self, product_id, quantity):
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

    # ---------------------- QUERY METHODS ----------------------
    @property
    def total_quantity(self):
        return CartItemModel.objects.filter(cart=self.cart).aggregate(
            total=Sum('quantity')
        )['total'] or 0

    def get_items_queryset(self):
        """
        Returns a queryset of CartItemModel with published products,
        ready for DRF serialization or internal logic.
        """
        return CartItemModel.objects.filter(
            cart=self.cart,
            product__status=ProductStatusType.publish.value
        ).select_related('product')

    def get_total_payment_amount(self):
        """
        Calculate total payment from queryset of published products.
        """
        qs = self.get_items_queryset()
        return sum(item.quantity * item.product.get_price() for item in qs)

    # ---------------------- SERIALIZATION METHODS ----------------------
    def get_cart_items(self):
        """
        Returns a list of CartItemModel objects for internal logic.
        Each item has access to 'product_obj' if needed.
        """
        return list(self.get_items_queryset())

    def serialize_items(self):
        """
        Returns a list of dicts for templates or DRF serialization.
        """
        items = []
        for item in self.get_items_queryset():
            price = item.product.get_price()
            items.append({
                "product_id": item.product.id,
                "product_name": item.product.title,
                "quantity": item.quantity,
                "unit_price": price,
                "total_price": item.quantity * price,
                "product_obj": item.product,  # optional for templates
            })
        return items
    @property
    def items(self):
        return self.get_items_queryset()

    def get_item(self, product_id):
        try:
            return self.get_items_queryset().get(product_id=product_id)
        except CartItemModel.DoesNotExist:
            return None
