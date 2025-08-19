from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from order.models import OrderModel, OrderItemModel, UserAddressModel, CouponModel
from cart.models import CartModel
from order.serializers import CheckoutSerializer, OrderSerializer, OrderDetailSerializer
from decimal import Decimal, ROUND_HALF_UP
from django.utils import timezone


class CheckoutAPIView(generics.GenericAPIView):
    serializer_class = CheckoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = request.user
        address = serializer.validated_data['address_id']
        coupon = serializer.validated_data.get('coupon_code')

        try:
            cart = CartModel.objects.get(user=user)
        except CartModel.DoesNotExist:
            return Response({"detail": "سبد خرید شما خالی است"}, status=status.HTTP_400_BAD_REQUEST)

        # Create order
        order = OrderModel.objects.create(
            user=user,
            address=address.address,
            state=address.state,
            city=address.city,
            zip_code=address.zip_code,
            coupon=coupon
        )

        # Create order items
        for item in cart.items.all():
            OrderItemModel.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.get_price(),
            )

        order.total_price = order.final_price_with_tax()
        order.save()

        if coupon:
            coupon.used_by.add(user)
            coupon.save()

        cart.items.all().delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class ValidateCouponAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        code = request.data.get('code')
        user = request.user

        try:
            coupon = CouponModel.objects.get(code=code)
        except CouponModel.DoesNotExist:
            return Response({"message": "کد تخفیف یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        if coupon.used_by.count() >= coupon.max_limit_usage:
            return Response({"message": "محدودیت در تعداد استفاده"}, status=status.HTTP_403_FORBIDDEN)

        if coupon.expiration_date and coupon.expiration_date < timezone.now():
            return Response({"message": "کد تخفیف منقضی شده است"}, status=status.HTTP_403_FORBIDDEN)

        if user in coupon.used_by.all():
            return Response({"message": "این کد تخفیف قبلا توسط شما استفاده شده است"}, status=status.HTTP_403_FORBIDDEN)

        try:
            cart = CartModel.objects.get(user=user)
        except CartModel.DoesNotExist:
            return Response({"message": "سبد خرید شما خالی است"}, status=status.HTTP_400_BAD_REQUEST)

        total = sum(Decimal(item.product.get_price()) * item.quantity for item in cart.items.all())
        discount_percent = Decimal(coupon.discount_percent) / Decimal('100')
        discount = (total * discount_percent).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
        discounted = total - discount
        tax = (discounted * Decimal('0.09')).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
        final = discounted + tax

        return Response({
            "message": "کد تخفیف با موفقیت اعمال شد.",
            "total_price": str(total),
            "discounted_price": str(discounted),
            "total_tax": str(tax),
            "final_price_with_tax": str(final)
        }, status=status.HTTP_200_OK)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = OrderModel.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return OrderSerializer
        return OrderDetailSerializer

    def get_queryset(self):
        user = self.request.user
        # Users can only see their own orders
        return OrderModel.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
