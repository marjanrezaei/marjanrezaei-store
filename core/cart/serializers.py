from rest_framework import serializers
from .models import CartItemModel

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.title')
    product_image = serializers.SerializerMethodField()
    unit_price = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItemModel
        fields = ['product_id', 'product_name', 'product_image', 'unit_price', 'quantity', 'total_price']

    def get_product_image(self, obj):
        if obj.product.image:
            return obj.product.image.url
        return '/static/img/default.jpg'

    def get_unit_price(self, obj):
        return obj.product.get_price()

    def get_total_price(self, obj):
        return obj.quantity * obj.product.get_price()
