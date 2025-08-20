from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions
from .models import OrderModel
from .serializers import OrderSerializer, CheckoutSerializer


class OrderStatusAPIView(generics.RetrieveAPIView):
    queryset = OrderModel.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        order = self.get_object()
        data = self.get_serializer(order).data
        return Response({
            'status': data['status'],
            'id': data['id'],
            'total_price': data['total_price'],
            'items': data['items'],
        })
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    
class OrderDetailAPIView(generics.RetrieveAPIView):
    queryset = OrderModel.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Ensure users can only see their own orders
        return self.queryset.filter(user=self.request.user)


class ValidateCouponAPIView(APIView):
    def post(self, request):
        serializer = CheckoutSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)  # Will validate coupon_code
        coupon = serializer.validated_data.get('coupon_code')

        # Here you can compute updated prices if you like
        order = OrderModel(user=request.user)  # dummy order for calculation
        total_price = order.total_price  # normally compute cart total
        discounted_price = total_price
        if coupon:
            discounted_price = total_price * (1 - coupon.discount_percent / 100)

        return Response({
            "message": "کد تخفیف معتبر است" if coupon else "کدی وارد نشده است",
            "total_price": total_price,
            "discounted_price": discounted_price,
            "total_tax": total_price * 0.09,
            "final_price_with_tax": discounted_price * 1.09
        })


