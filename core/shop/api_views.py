# shop/api_views.py
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import FieldError
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from parler.views import TranslatableSlugMixin

from .models import ProductModel, ProductStatusType, WishlistProductModel
from .serializers import ProductSerializer, ProductDetailSerializer


class ProductDetailBySlugAPIView(TranslatableSlugMixin, RetrieveAPIView):
    queryset = ProductModel.objects.filter(status=ProductStatusType.publish.value)
    serializer_class = ProductDetailSerializer
    slug_field = "slug"          
    slug_url_kwarg = "slug"      
    

class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = ProductModel.objects.filter(status=ProductStatusType.publish.value)

        search_q = self.request.GET.get("q")
        category_id = self.request.GET.get("category_id")
        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")
        order_by = self.request.GET.get("order_by")

        if search_q:
            queryset = queryset.filter(title__icontains=search_q)
            
        if category_id:
            queryset = queryset.filter(category__id=category_id)

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        if order_by:
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass

        return queryset


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = ProductModel.objects.filter(status=ProductStatusType.publish.value)
    serializer_class = ProductDetailSerializer
    lookup_field = "id"


class WishlistToggleAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_id = request.data.get("product_id")
        message = ""
        if product_id:
            try:
                wishlist_item = WishlistProductModel.objects.get(
                    user=request.user, product__id=product_id)
                wishlist_item.delete()
                message = "محصول از لیست علایق حذف شد"
            except WishlistProductModel.DoesNotExist:
                WishlistProductModel.objects.create(
                    user=request.user, product_id=product_id)
                message = "محصول به لیست علایق اضافه شد"
        return Response({"message": message}, status=status.HTTP_200_OK)
