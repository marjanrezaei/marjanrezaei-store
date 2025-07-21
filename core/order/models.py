from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal, ROUND_HALF_UP
from django.utils.translation import gettext_lazy as _


class OrderStatusType(models.IntegerChoices):
    PENDING = 1, _("در انتظار پرداخت")
    SUCCESS = 2, _("موفقیت آمیز")
    FAILED = 3, _("لغو شده")


class UserAddressModel(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    address = models.CharField(max_length=250)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.address}"


class CouponModel(models.Model):
    code = models.CharField(max_length=100, unique=True)
    discount_percent = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    max_limit_usage = models.PositiveIntegerField(default=10)
    used_by = models.ManyToManyField('accounts.User', related_name="coupon_users", blank=True)

    expiration_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

    def used_by_count(self):
        return self.used_by.count()

    def used_by_list(self):
        return ", ".join(user.email for user in self.used_by.all())


class OrderModel(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.PROTECT)

    # Shipping address details
    address = models.CharField(max_length=250)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)

    payment = models.ForeignKey('payment.PaymentModel', on_delete=models.SET_NULL, null=True, blank=True)
    coupon = models.ForeignKey(CouponModel, on_delete=models.PROTECT, null=True, blank=True)

    total_price = models.DecimalField(default=0, max_digits=10, decimal_places=0)
    status = models.IntegerField(choices=OrderStatusType.choices, default=OrderStatusType.PENDING)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - Order #{self.id}"

    def calculate_total_price(self):
        return sum(item.price * item.quantity for item in self.order_items.all())

    def calculate_discount(self):
        if not self.coupon:
            return Decimal('0')
        discount_percent = Decimal(str(self.coupon.discount_percent)) / Decimal('100')
        return (self.calculate_total_price() * discount_percent).quantize(Decimal('1'), rounding=ROUND_HALF_UP)

    def calculate_tax(self):
        taxed_subtotal = self.calculate_total_price() - self.calculate_discount()
        return (taxed_subtotal * Decimal('0.09')).quantize(Decimal('1'), rounding=ROUND_HALF_UP)

    def final_price_with_tax(self):
        subtotal = self.calculate_total_price()
        discount = self.calculate_discount()
        return (subtotal - discount + self.calculate_tax()).quantize(Decimal('1'), rounding=ROUND_HALF_UP)

    def get_status(self):
        try:
            status_enum = OrderStatusType(self.status)
            return {
                "id": self.status,
                "title": status_enum.name,
                "label": status_enum.label,
            }
        except ValueError:
            return {
                "id": self.status,
                "title": "UNKNOWN",
                "label": _("وضعیت نامعتبر"),
            }

    def get_full_address(self):
        return f"{self.state}, {self.city}, {self.address}"

    @property
    def is_successful(self):
        return self.status == OrderStatusType.SUCCESS.value


class OrderItemModel(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey('shop.ProductModel', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.title} × {self.quantity} (Order #{self.order.id})"
