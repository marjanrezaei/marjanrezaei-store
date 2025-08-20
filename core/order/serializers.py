from rest_framework import serializers
from django.utils import timezone

from order.models import UserAddressModel, CouponModel, OrderModel, OrderItemModel


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddressModel
        fields = ['id', 'address', 'state', 'city', 'zip_code']


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouponModel
        fields = ['code', 'discount_percent', 'max_limit_usage', 'expiration_date']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItemModel
        fields = ['product', 'quantity', 'price']


class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItemModel
        fields = ['id', 'product', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    coupon = CouponSerializer(read_only=True)

    class Meta:
        model = OrderModel
        fields = [
            'id', 'user', 'address', 'state', 'city', 'zip_code',
            'coupon', 'total_price', 'status', 'items', 'created_at'
        ]


class CheckoutSerializer(serializers.Serializer):
    address_id = serializers.IntegerField()
    coupon_code = serializers.CharField(required=False, allow_blank=True)

    def validate_address_id(self, value):
        user = self.context['request'].user
        try:
            address = UserAddressModel.objects.get(id=value, user=user)
        except UserAddressModel.DoesNotExist:
            raise serializers.ValidationError("Invalid address for the requested user.")
        return address

    def validate_coupon_code(self, value):
        user = self.context['request'].user
        if not value:
            return None
        try:
            coupon = CouponModel.objects.get(code=value)
        except CouponModel.DoesNotExist:
            raise serializers.ValidationError("کد تخفیف اشتباه است")

        if coupon.used_by.count() >= coupon.max_limit_usage:
            raise serializers.ValidationError("محدودیت در تعداد استفاده")

        if coupon.expiration_date and coupon.expiration_date < timezone.now():
            raise serializers.ValidationError("کد تخفیف منقضی شده است")

        if user in coupon.used_by.all():
            raise serializers.ValidationError("این کد تخفیف قبلا توسط شما استفاده شده است")

        return coupon


class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True)

    class Meta:
        model = OrderModel
        fields = [
            'id', 'user', 'address', 'state', 'city', 'zip_code',
            'coupon', 'total_price', 'status', 'items', 'created_at'
        ]
        read_only_fields = ['user', 'total_price', 'status', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        order = OrderModel.objects.create(**validated_data)
        for item_data in items_data:
            OrderItemModel.objects.create(order=order, **item_data)
        order.total_price = order.final_price_with_tax()
        order.save()
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.items.all().delete()
        for item_data in items_data:
            OrderItemModel.objects.create(order=instance, **item_data)
        instance.total_price = instance.final_price_with_tax()
        instance.save()
        return instance
