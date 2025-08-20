from django.urls import path
from .. import views

urlpatterns = [
    path("addresses/", views.CustomerAddressManageView.as_view(), name="address-list"),
]
