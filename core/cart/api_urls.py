from django.urls import path
from . import api_views

app_name = "cart_api"

urlpatterns = [
    path("add/<int:product_id>/", api_views.AddToCartAPIView.as_view(), name="add-to-cart-api"),
    path("remove-product/", api_views.RemoveProductAPIView.as_view(), name="remove-product-api"),
    path("update-product-quantity/", api_views.UpdateProductQuantityAPIView.as_view(), name="update-product-quantity-api"),
    path("summary/", api_views.CartSummaryAPIView.as_view(), name="cart-summary-api"),
]
