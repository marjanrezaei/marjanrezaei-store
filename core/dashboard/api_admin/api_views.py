from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from order.models import CouponModel, OrderModel
from shop.models import ProductModel
from review.models import ReviewModel
from dashboard.permissions import IsAdminUser
from accounts.models import Profile
from .serializers import (
    CouponSerializer, OrderSerializer,
    ProductSerializer, ReviewSerializer,
    ProfileSerializer
)


class AdminDashboardAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        data = {
            "user_count": Profile.objects.count(),
            "order_count": OrderModel.objects.count(),
            "product_count": ProductModel.objects.count(),
            "review_count": ReviewModel.objects.count(),
            "coupon_count": CouponModel.objects.count(),
        }
        return Response(data)


# ---------- Coupons ----------
class CouponViewSet(viewsets.ModelViewSet):
    serializer_class = CouponSerializer
    queryset = CouponModel.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['code']
    ordering_fields = ['created_at', 'discount_percent']


# ---------- Orders ----------
class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    queryset = OrderModel.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['created_at', 'status']

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.query_params.get("status")
        if status:
            queryset = queryset.filter(status=status)
        return queryset


# ---------- Products ----------
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = ProductModel.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['price', 'created_at']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()


# ---------- Reviews ----------
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = ReviewModel.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['product__title']
    ordering_fields = ['created_at', 'status']


# ---------- Profile ----------
class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)
