from django.contrib import admin
from .models import OrderModel, OrderItemModel, CouponModel, UserAddressModel


@admin.register(OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "total_price",
        "coupon",
        "status",
        "created_at"
    )


@admin.register(OrderItemModel)
class OrderItemModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "product",
        "quantity",
        "price",
        "created_at"
    )


@admin.register(CouponModel)
class CouponModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "code",
        "discount_percent",
        "max_limit_usage",
        "used_by_count",  # This is calling the method below
        "expiration_date",
        "created_at"
    )

    @admin.display(description='Used By Count')
    def used_by_count(self, obj):
        return obj.used_by.count()


@admin.register(UserAddressModel)
class UserAddressModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "address",
        "state",
        "city",
        "zip_code",
        "created_at"
    )
