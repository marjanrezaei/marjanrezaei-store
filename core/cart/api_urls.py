from django.urls import path
from . import api_views

app_name = "cart_api"

urlpatterns = [
    path("add/<int:product_id>/", api_views.AddToCartAPIView.as_view(), name="add_to_cart_api"),
    path("remove-product/", api_views.RemoveProductView.as_view(), name="api_remove_product"),
    path("update/", api_views.UpdateProductQuantityView.as_view(), name="update-cart"),
    path("summary/", api_views.CartSummaryAPIView.as_view(), name="cart-summary"),
]
