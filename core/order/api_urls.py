from django.urls import path
from . import api_views

app_name = "order_api"

urlpatterns = [
    path("validate-coupon/", api_views.ValidateCouponAPIView.as_view(), name="validate-coupon-api"),
    path('<int:pk>/detail/', api_views.OrderDetailAPIView.as_view(), name='order-detail-api'),
    path('<int:pk>/status/', api_views.OrderStatusAPIView.as_view(), name='order-status-api'),

]
