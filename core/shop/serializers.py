# shop/serializers.py
from rest_framework import serializers
from .models import ProductModel, ProductCategoryModel


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = ProductModel
        fields = ["id", "title", "price", "category", "image"]


class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = ProductModel
        fields = ["id", "title", "description", "price", "category", "image", "reviews"]

    def get_reviews(self, obj):
        return [
            {
                "user": review.user.username,
                "text": review.text,
                "rating": review.rating,
            }
            for review in obj.reviews.filter(status=1)  # فقط accepted
        ]
