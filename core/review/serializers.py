from rest_framework import serializers
from .models import ReviewModel, ReviewStatusType
from shop.models import ProductModel, ProductStatusType


class ReviewSerializer(serializers.ModelSerializer):
    status_display = serializers.SerializerMethodField()

    class Meta:
        model = ReviewModel
        fields = [
            "id", "user", "product", "description", "rate",
            "status", "status_display", "created_at", "updated_at"
        ]
        read_only_fields = ["user", "status", "created_at", "updated_at"]

    def get_status_display(self, obj):
        return obj.get_status()

    def validate_product(self, product):
        if not ProductModel.objects.filter(
            id=product.id, status=ProductStatusType.publish.value
        ).exists():
            raise serializers.ValidationError("این محصول وجود ندارد یا منتشر نشده است.")
        return product

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
