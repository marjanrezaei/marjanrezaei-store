from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import FieldError
from django.http import JsonResponse

from .models import (
    ProductModel,
    ProductStatusType,
    ProductCategoryModel,
    WishlistProductModel,
)


class ShopProductGridView(ListView):
    template_name = "shop/product-grid.html"
    model = ProductModel
    paginate_by = 9

    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_items"] = self.get_queryset().count()
        context["categories"] = ProductCategoryModel.objects.all()
        context["wishlist_items"] = self._get_user_wishlist()
        return context

    def _get_user_wishlist(self):
        user = self.request.user
        if user.is_authenticated:
            return WishlistProductModel.objects.filter(user=user).values_list('product__id', flat=True)
        return []


class ShopProductDetailView(DetailView):
    template_name = "shop/product-detail.html"
    queryset = ProductModel.objects.filter(status=ProductStatusType.publish.value)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_wished"] = self._is_product_wished()
        return context

    def _is_product_wished(self):
        user = self.request.user
        if user.is_authenticated:
            return WishlistProductModel.objects.filter(user=user, product=self.get_object()).exists()
        return False


class AddOrRemoveWishlistView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get("product_id")
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

        return JsonResponse({"message": message})