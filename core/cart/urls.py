from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path("cart/add/<int:product_id>/", views.AddToCartView.as_view(), name="add-to-cart"),
    path("remove-product/", views.RemoveProductView.as_view(), name="remove-product"),
    path("update-product-quantity/", views.UpdateProductQuantityView.as_view(), name="update-product-quantity"),
    path("summary/", views.CartSummaryView.as_view(), name="cart-summary"),
]