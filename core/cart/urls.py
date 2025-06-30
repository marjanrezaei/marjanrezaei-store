from django.urls import path, re_path
from . import views

app_name = 'cart'

urlpatterns = [
    path("db/add-product/", views.DBAddProductView.as_view(), name="db-add-product"),
    path("db/remove-product/", views.DBRemoveProductView.as_view(), name="db-remove-product"),
    path("db/update-product-quantity/", views.DBUpdateProductQuantityView.as_view(), name="db-update-product-quantity"),
    path("db/cart/summary/", views.DBCartSummaryView.as_view(), name="db-cart-summary"),
]
