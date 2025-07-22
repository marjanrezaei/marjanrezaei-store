from django.views.generic import UpdateView,DeleteView,CreateView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import CustomerRequiredMixin

from dashboard.customer.forms import *
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import FieldError
from shop.models import WishlistProductModel

class CustomerWishlistListView(LoginRequiredMixin, CustomerRequiredMixin, ListView):
    template_name = "dashboard/customer/wishlists/wishlist-list.html"
    paginate_by = 2

    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)
    
    def get_queryset(self):
        queryset = WishlistProductModel.objects.filter(user=self.request.user)
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(product__title__icontains=search_q)
        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_items"] = self.get_queryset().count()
        return context

class CustomerWishlistDeleteView(LoginRequiredMixin, CustomerRequiredMixin, SuccessMessageMixin, DeleteView):
    http_method_names = ["post"]
    success_url = reverse_lazy("dashboard:customer:wishlist-list")
    success_message = "Wishlist item deleted successfully"
    def get_queryset(self):
        return WishlistProductModel.objects.filter(user=self.request.user)
