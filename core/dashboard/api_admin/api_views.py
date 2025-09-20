from rest_framework import viewsets, filters, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from order.models import CouponModel, OrderModel
from shop.models import ProductModel, ProductCategoryModel
from review.models import ReviewModel
from dashboard.permissions import IsAdminUser
from accounts.models import Profile
from .serializers import (
    CouponSerializer, OrderSerializer,
    ProductSerializer, ReviewSerializer,
    ProfileSerializer, ProductCategorySerializer
)
from core.mixins import SwaggerSafeMixin


class AdminDashboardAPIView(APIView):
    """Provide counts for admin dashboard"""
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def get(self, request):
        data = {
            "user_count": Profile.objects.count(),
            "order_count": OrderModel.objects.count(),
            "product_count": ProductModel.objects.count(),
            "review_count": ReviewModel.objects.count(),
            "coupon_count": CouponModel.objects.count(),
        }
        return Response(data)


class CouponViewSet(viewsets.ModelViewSet):
    """Manage coupons (Admin only)"""
    serializer_class = CouponSerializer
    queryset = CouponModel.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['code']
    ordering_fields = ['created_at', 'discount_percent']


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    """View orders with filtering (Admin only)"""
    serializer_class = OrderSerializer
    queryset = OrderModel.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['created_at', 'status']

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.query_params.get("status")
        if status:
            queryset = queryset.filter(status=status)
        return queryset


class ProductViewSet(SwaggerSafeMixin, viewsets.ModelViewSet):
    """Manage products (Admin only)"""
    serializer_class = ProductSerializer
    queryset = ProductModel.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['price', 'created_at']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()


class ReviewViewSet(viewsets.ModelViewSet):
    """Manage product reviews (Admin only)"""
    serializer_class = ReviewSerializer
    queryset = ReviewModel.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['product__title']
    ordering_fields = ['created_at', 'status']


class ProfileViewSet(SwaggerSafeMixin, viewsets.ModelViewSet):
    """Manage user profiles (Admin only)"""
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    queryset = Profile.objects.all()
    
    def get_queryset(self):
        qs = super().get_queryset()
        if hasattr(self.request, 'user') and self.request.user.is_authenticated:
            return qs.filter(user=self.request.user)
        return qs.none()


# -------------------- Category --------------------
class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategoryModel.objects.all()
    serializer_class = ProductCategorySerializer

