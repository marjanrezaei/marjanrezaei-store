from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
)
from .models import ProductModel, ProductStatusType


class ShopProductGridView(ListView):
    template_name = "shop/product-grid.html"
    model = ProductModel
    paginate_by = 9

    def get_queryset(self):
        return super().get_queryset().filter(status=ProductStatusType.publish.value)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_items"] = self.get_queryset().count()
        return context