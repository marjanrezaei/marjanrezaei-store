from django.db import models


class CartModel(models.Model):
    user = models.OneToOneField(
        "accounts.User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        unique=True,
    )
    session_key = models.CharField(max_length=40, null=True, blank=True, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user:
            return f"Cart of {self.user.email}"
        return f"Cart for session {self.session_key}"
    
    def calculate_total_price(self):
        return sum(item.product.get_price()* item.quantity for item in self.items.all())


class CartItemModel(models.Model):
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('shop.ProductModel', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.product.title} - {self.cart.id}"
