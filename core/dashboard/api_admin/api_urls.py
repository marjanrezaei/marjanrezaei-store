from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'coupons', api_views.CouponViewSet, basename='admin-coupons')
router.register(r'orders', api_views.OrderViewSet, basename='admin-orders')
router.register(r'products', api_views.ProductViewSet, basename='admin-products')
router.register(r'reviews', api_views.ReviewViewSet, basename='admin-reviews')
router.register(r'profile', api_views.ProfileViewSet, basename='admin-profile')

urlpatterns = [
    path('', api_views.AdminDashboardAPIView.as_view(), name='admin-dashboard-api'),

    path('', include(router.urls)),
]
