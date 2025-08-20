from django.urls import path
from . import api_views

app_name = "payment_api"

urlpatterns = [
    path("verify/", api_views.PaymentVerifyAPIView.as_view(), name="payment_verify"),
]
