from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class ShopProductGridView(TemplateView):
    template_name = "shop/product-grid.html"
