from django.views.generic import (
    UpdateView, 
    ListView, 
    DeleteView, 
    CreateView
    )
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import AdminRequiredMixin
from dashboard.admin.forms import  ProductForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import FieldError

from shop.models import ProductModel, ProductCategoryModel, ProductImageModel
from core.utils.liara_upload import upload_to_liara


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
        return context

class AdminProductCreateView(AdminRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "dashboard/admin/products/product-create.html"
    queryset = ProductModel.objects.all()
    form_class = ProductForm
    success_message = "ایجاد محصول با موفقیت انجام شد"

    def form_valid(self, form):
        form.instance.user = self.request.user
        image_file = self.request.FILES.get("image")

        if image_file:
            filename = f"{form.instance.slug}_{image_file.name}"
            image_url = upload_to_liara(image_file, filename, folder="products")
            form.instance.image_url = image_url
            form.instance.image = None  

        response = super().form_valid(form)

        # ذخیره تصاویر اضافی
        for extra_file in self.request.FILES.getlist("extra_images"):
            filename = f"{form.instance.slug}_{extra_file.name}"
            image_url = upload_to_liara(extra_file, filename, folder="products/extra")
            ProductImageModel.objects.create(product=form.instance, file=image_url)

        return response

    def get_success_url(self):
        return reverse_lazy("dashboard:admin:product-edit", kwargs={"pk": self.object.pk})


class AdminProductEditView(AdminRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "dashboard/admin/products/product-edit.html"
    queryset = ProductModel.objects.all()
    form_class = ProductForm
    success_message = "ویرایش محصول با موفقیت انجام شد"

    def form_valid(self, form):
        product = form.instance
        host = self.request.get_host()

        # ذخیره تصویر اصلی محصول
        main_image = self.request.FILES.get("image")
        if main_image:
            filename = f"{product.id}_{main_image.name}"
            if "onrender.com" in host:
                image_url = upload_to_liara(main_image, filename, folder="products")
                product.image_url = image_url
                product.image = None
            else:
                product.image.save(filename, main_image)

        response = super().form_valid(form)

        # ذخیره تصاویر اضافی محصول
        extra_images = self.request.FILES.getlist("extra_images")
        for extra_file in extra_images:
            filename = f"{product.id}_extra_{extra_file.name}"
            if "onrender.com" in host:
                image_url = upload_to_liara(extra_file, filename, folder="products/extra")
                ProductImageModel.objects.create(product=product, file=image_url)
            else:
                image_instance = ProductImageModel(product=product)
                image_instance.file.save(filename, extra_file)

        return response

    def get_success_url(self):
        return reverse_lazy("dashboard:admin:product-edit", kwargs={"pk": self.object.pk})


class AdminProductDeleteView(AdminRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = "dashboard/admin/products/product-delete.html"
    queryset = ProductModel.objects.all()
    success_url = reverse_lazy("dashboard:admin:product-list")
    success_message = "حذف محصول با  موفقیت انجام شد"  

    
class AdminProductImageDeleteView(AdminRequiredMixin, LoginRequiredMixin, DeleteView):
    model = ProductImageModel
    success_message = "تصویر حذف شد"

    def get_success_url(self):
        return reverse_lazy("dashboard:admin:product-edit", kwargs={"pk": self.object.product.pk})