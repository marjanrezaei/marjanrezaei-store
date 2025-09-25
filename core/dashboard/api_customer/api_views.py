from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from order.models import UserAddressModel, OrderModel
from shop.models import WishlistProductModel
from accounts.models import Profile
from .serializers import (
    CustomerAddressSerializer,
    OrderSerializer,
    CustomerProfileSerializer,
    CustomerWishlistSerializer,
    CustomerProfileImageSerializer,
)
from core.mixins import SwaggerSafeMixin


# -------------------------
# Addresses
# -------------------------
class CustomerAddressViewSet(SwaggerSafeMixin, viewsets.ModelViewSet):
    serializer_class = CustomerAddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserAddressModel.objects.all()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(user=self.request.user)
        return self.queryset.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# -------------------------
# Orders
# -------------------------
class CustomerOrderViewSet(SwaggerSafeMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = OrderModel.objects.all()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(user=self.request.user).order_by('-created_at')
        return self.queryset.none()

    @action(detail=True, methods=['get'])
    def invoice(self, request, pk=None):
        order = self.get_object()
        if order.status != OrderModel.Status.SUCCESS.value:
            return Response(
                {"detail": _("Invoice only available for successful orders")},
                status=400
            )
        serializer = self.get_serializer(order)
        return Response(serializer.data)


# -------------------------
# Profile
# -------------------------
class CustomerProfileViewSet(SwaggerSafeMixin, viewsets.GenericViewSet):
    serializer_class = CustomerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.all()

    def get_object(self):
        if getattr(self, 'swagger_fake_view', False):
            return Profile()
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def retrieve(self, request):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)

    def update(self, request):
        serializer = self.get_serializer(
            self.get_object(),
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['post'],
        serializer_class=CustomerProfileImageSerializer,
        parser_classes=[MultiPartParser, FormParser]
    )
    def upload_image(self, request):
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": _("Profile image updated successfully")})


# -------------------------
# Wishlist
# -------------------------
class CustomerWishlistViewSet(SwaggerSafeMixin, viewsets.ModelViewSet):
    serializer_class = CustomerWishlistSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = WishlistProductModel.objects.all()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(user=self.request.user)
        return self.queryset.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
