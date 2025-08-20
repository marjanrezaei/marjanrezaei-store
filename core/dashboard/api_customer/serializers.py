from rest_framework import serializers
from order.models import UserAddressModel, OrderModel, OrderItemModel, OrderStatusType
from accounts.models import Profile
from shop.models import WishlistProductModel
from core.utils.liara_upload import upload_to_liara


# Addresses
class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddressModel
        fields = ['id', 'address', 'state', 'city', 'zip_code']


# Orders
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItemModel
        fields = ['id', 'product', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderModel
        fields = ['id', 'status', 'created_at', 'updated_at', 'items', 'total_price']

    def get_total_price(self, obj):
        return sum(item.price * item.quantity for item in obj.items.all())


# Profile
class CustomerProfileSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone_number', 'image_url']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image_url:
            return obj.image_url
        elif obj.image and hasattr(obj.image, 'url'):
            if request is not None:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

    
class CustomerProfileImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True, required=True)

    class Meta:
        model = Profile
        fields = ['image']

    def update(self, instance, validated_data):
        image_file = validated_data.get('image')
        if image_file:
            host = self.context['request'].get_host()
            filename = f"profile/{instance.user.id}_{image_file.name}"

            # Liara vs local storage
            if host == "marjanrezaei-store.onrender.com":
                instance.image_url = upload_to_liara(image_file, filename)
            else:
                instance.image.save(filename, image_file)
            instance.save()
        return instance

    
# Wishlist
class CustomerWishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistProductModel
        fields = ['id', 'product']


# Password Change
class CustomerPasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password1 = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)
