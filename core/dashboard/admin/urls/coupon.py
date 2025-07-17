from django.urls import path
from .. import views

urlpatterns = [  
    path("coupon/list/", views.AdminCouponListView.as_view(), name="coupon-list"),
    path("coupon/create/", views.AdminCouponCreateView.as_view(), name="coupon-create"),
    path("coupon/<int:pk>/edit/", views.AdminCouponEditView.as_view(), name="coupon-edit"),
    path("coupon/<int:pk>/delete/", views.AdminCouponDeleteView.as_view(), name="coupon-delete"),  
    
    path("coupon/used/", views.CouponUsedListView.as_view(), name="coupon-used-by"),
    ]