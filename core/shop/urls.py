from django.urls import path, re_path
from . import views

app_name = 'shop'

urlpatterns = [
    path('product/grid/', views.ShopProductGridView.as_view(), name='product-grid'),
    path('product/<slug:slug>/detail/', views.ShopProductDetailView.as_view(), name='product-detail'),
    re_path(r'product/(?P<slug>[-\w]+)/detail/', views.ShopProductDetailView.as_view(), name='product-detail'),

]
