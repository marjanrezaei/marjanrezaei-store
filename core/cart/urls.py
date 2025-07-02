from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path("cart/add/<int:product_id>/", views.AddToCartView.as_view(), name="db-add-product"),
    path("remove-product/", views.RemoveProductView.as_view(), name="db-remove-product"),
    path("cart/update-product-quantity/", views.UpdateProductQuantityView.as_view(), name="db-update-product-quantity"),
    path("summary/", views.CartSummaryView.as_view(), name="db-cart-summary"),
]