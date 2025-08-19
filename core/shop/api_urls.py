from django.urls import path
from . import api_views

app_name = "shop_api"

urlpatterns = [
    path("products/", api_views.ProductListAPIView.as_view(), name="product_list_api"),
    path("products/<int:id>/", api_views.ProductDetailAPIView.as_view(), name="product_detail_api"),
    path("wishlist/toggle/", api_views.WishlistToggleAPIView.as_view(), name="wishlist_toggle_api"),
]
