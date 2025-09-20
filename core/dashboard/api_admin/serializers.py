from rest_framework import serializers
from order.models import CouponModel, OrderModel
from shop.models import ProductModel, ProductImageModel, ProductCategoryModel
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


 # -------------------- Category --------------------
class ProductCategorySerializer(serializers.ModelSerializer):
    translations = serializers.DictField(write_only=True, required=False)
    all_translations = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProductCategoryModel
        fields = ["id", "all_translations", "translations"]

    def get_all_translations(self, obj):
        return {lang: {
                    "title": obj.safe_translation_getter("title", language_code=lang),
                    "slug": obj.safe_translation_getter("slug", language_code=lang),
                } for lang in ["fa", "en", "ar"]}

    def create(self, validated_data):
        translations = validated_data.pop("translations", {})
        category = ProductCategoryModel.objects.create(**validated_data)
        for lang, data in translations.items():
            category.set_current_language(lang)
            category.title = data.get("title", "")
            category.slug = data.get("slug", "")
            category.save()
        return category

    def update(self, instance, validated_data):
        translations = validated_data.pop("translations", {})
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        for lang, data in translations.items():
            instance.set_current_language(lang)
            instance.title = data.get("title", instance.title)
            instance.slug = data.get("slug", instance.slug)
            instance.save()
        return instance
