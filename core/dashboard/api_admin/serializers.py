from rest_framework import serializers
from order.models import CouponModel, OrderModel
from shop.models import ProductModel, ProductImageModel
from review.models import ReviewModel
from accounts.models import Profile


# ---------- Coupons ----------
class CouponSerializer(serializers.ModelSerializer):
    used_by_count = serializers.IntegerField(source='used_by.count', read_only=True)

    class Meta:
        model = CouponModel
        fields = [
            'id', 'code', 'discount_percent', 'max_limit_usage',
            'expiration_date', 'used_by_count'
        ]
        ref_name = "AdminCouponSerializer"


# ---------- Orders ----------
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = '__all__'
        ref_name = "AdminOrderSerializer"


# ---------- Products ----------
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImageModel
        fields = ['id', 'url']


class ProductSerializer(serializers.ModelSerializer):
    extra_images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = ProductModel
        fields = [
            'id', 'category', 'title', 'slug', 'image_url',
            'description', 'breif_description', 'stock', 'status',
            'price', 'discount_percent', 'extra_images'
        ]
        ref_name = "AdminProductSerializer"


# ---------- Reviews ----------
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewModel
        fields = '__all__'
        ref_name = "AdminReviewSerializer"


# ---------- Profile ----------
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'image_url']
        ref_name = "AdminProfileSerializer"

