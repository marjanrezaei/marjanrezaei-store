from django.views.generic import (
    UpdateView, 
    ListView, 
    DeleteView, 
    CreateView
    )
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import AdminRequiredMixin
from django.contrib.auth import views as auth_views
from dashboard.admin.forms import AdminPasswordChangeForm, AdminProfileEditForm, ProductForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.exceptions import FieldError

from accounts.models import Profile
from shop.models import ProductModel, ProductStatusType, ProductCategoryModel




class AdminProductListView(AdminRequiredMixin, LoginRequiredMixin, ListView):
    template_name = "dashboard/admin/products/product-list.html"
    model = ProductModel
    queryset = ProductModel.objects.all()
    paginate_by = 10

    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)

    def get_queryset(self):
        queryset= ProductModel.objects.all()
        if search_q:=self.request.GET.get("q"):
            queryset = queryset.filter(title__icontains=search_q)
        if category_id:=self.request.GET.get("category_id"):
            queryset = queryset.filter(category__id=category_id)
        if  min_price:=self.request.GET.get("min_price"):
            queryset = queryset.filter(price__gte=min_price)
        if  max_price:=self.request.GET.get("max_price"):
            queryset = queryset.filter(price__lte=max_price)
        if  order_by:=self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_items"] = self.queryset.count()
        context["categories"] = ProductCategoryModel.objects.all()
        self.request.session['fav_color'] = 'blue'
        return context

class AdminProductCreateView(AdminRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "dashboard/admin/products/product-create.html"
    queryset = ProductModel.objects.all()
    form_class = ProductForm
    success_message = "ایجاد محصول با  موفقیت انجام شد"
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        super().form_valid(form)
        return redirect(reverse_lazy("dashboard:admin:product-edit", kwargs={"pk": form.instance.pk}))
    
    def get_success_url(self):
        return reverse_lazy("dashboard:admin:product-list") 
    

class AdminProductEditView(AdminRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "dashboard/admin/products/product-edit.html"
    queryset = ProductModel.objects.all()
    form_class = ProductForm
    success_message = "ویرایش محصول با  موفقیت انجام شد"
    
    def get_success_url(self):
        return reverse_lazy("dashboard:admin:product-edit", kwargs={"pk":self.get_object().pk})


class AdminProductDeleteView(AdminRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = "dashboard/admin/products/product-delete.html"
    queryset = ProductModel.objects.all()
    success_url = reverse_lazy("dashboard:admin:product-list")
    success_message = "حذف محصول با  موفقیت انجام شد"  
    