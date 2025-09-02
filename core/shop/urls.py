from django.urls import path, re_path, include
from . import views

app_name = 'shop'

urlpatterns = [
    path('product/list/', views.ShopProductGridView.as_view(), name='product-list'),
    re_path(r'product/(?P<slug>[-\w]+)/detail/', views.ShopProductDetailView.as_view(), name='product-detail'),
    path('add-or-remove-wishlist/', views.AddOrRemoveWishlistView.as_view(), name='add-or-remove-wishlist'),
]
