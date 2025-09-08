from rest_framework import serializers
from .models import ProductModel
from django.utils import translation


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    title = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductModel
        fields = ["id", "title", "price", "category", "image"]
        ref_name = "ShopProductSerializer"
    
    def get_title(self, obj):
        lang = translation.get_language() 
        return getattr(obj, f"title_{lang}", obj.title)


class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = ProductModel
        fields = ["id", "title", "description", "price", "category", "image", "reviews"]

    def get_title(self, obj):
        lang = translation.get_language()
        return getattr(obj, f"title_{lang}", obj.title)

    def get_description(self, obj):
        lang = translation.get_language()
        return getattr(obj, f"description_{lang}", obj.description)
    
    def get_reviews(self, obj):
        return [
            {
                "user": review.user.username,
                "text": review.text,
                "rating": review.rating,
            }
            for review in obj.reviews.filter(status=1)  
        ]
