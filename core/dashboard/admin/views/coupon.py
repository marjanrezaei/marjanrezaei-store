from django.views.generic import (
    UpdateView, 
    ListView, 
    DeleteView, 
    CreateView
    )
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import AdminRequiredMixin
from dashboard.admin.forms import CouponForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _

from order.models import CouponModel


class AdminCouponListView(AdminRequiredMixin, LoginRequiredMixin, ListView):
    template_name = "dashboard/admin/coupon/coupon-list.html"
    model = CouponModel
    queryset = CouponModel.objects.all()
    paginate_by = 10

    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        order_by = self.request.GET.get('order_by')
        q = self.request.GET.get('q')
        if order_by in ['created_at', '-created_at', 'discount_percent', '-discount_percent']:
            queryset = queryset.order_by(order_by)
        if q:
            queryset = queryset.filter(code__icontains=q)
            
        return queryset
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        coupons = context["object_list"]  
        
        for coupon in coupons:
            coupon.used_by_count = coupon.used_by.count()

        return context
     

class AdminCouponCreateView(AdminRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = "dashboard/admin/coupon/coupon-create.html"
    queryset = CouponModel.objects.all()
    form_class = CouponForm
    success_message = _("Coupon created successfully")  

    def form_valid(self, form):
        # Assign the currently logged-in user to the coupon
        form.instance.user = self.request.user
        super().form_valid(form)
        # Redirect to edit page after creation
        return redirect(reverse_lazy("dashboard:admin:coupon-edit", kwargs={"pk": form.instance.pk}))

    def get_success_url(self):
        # Fallback success URL after form submission
        return reverse_lazy("dashboard:admin:coupon-list")    


class AdminCouponEditView(AdminRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "dashboard/admin/coupon/coupon-edit.html"
    queryset = CouponModel.objects.all()
    form_class = CouponForm
    success_message = _("Coupon updated successfully") 

    def get_success_url(self):
        # Return the edit page of the current coupon
        return reverse_lazy("dashboard:admin:coupon-edit", kwargs={"pk": self.get_object().pk})


class AdminCouponDeleteView(AdminRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = "dashboard/admin/coupon/coupon-delete.html"
    queryset = CouponModel.objects.all()
    success_url = reverse_lazy("dashboard:admin:coupon-list")
    success_message = _("Coupon deleted successfully") 
    

class CouponUsedListView(AdminRequiredMixin, LoginRequiredMixin, ListView):
    template_name = "dashboard/admin/coupon/coupon-used.html"
    model = CouponModel
    queryset = CouponModel.objects.all()
    paginate_by = 10

    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        order_by = self.request.GET.get('order_by')
        q = self.request.GET.get('q')
        if order_by in ['created_at', '-created_at', 'discount_percent', '-discount_percent']:
            queryset = queryset.order_by(order_by)
        if q:
            queryset = queryset.filter(code__icontains=q)
            
        return queryset