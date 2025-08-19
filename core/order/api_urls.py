from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

app_name = "order_api"

router = DefaultRouter()
router.register(r"orders", api_views.OrderViewSet, basename="orders")

urlpatterns = [
    path("checkout/", api_views.CheckoutAPIView.as_view(), name="checkout"),
    path("validate-coupon/", api_views.ValidateCouponAPIView.as_view(), name="validate_coupon"),
    path("", include(router.urls)),
]
