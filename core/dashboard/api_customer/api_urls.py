from rest_framework.routers import DefaultRouter
from . import api_views
router = DefaultRouter()
router.register(r'addresses', api_views.CustomerAddressViewSet, basename='customer-addresses')
router.register(r'orders', api_views.CustomerOrderViewSet, basename='customer-orders')
router.register(r'profile', api_views.CustomerProfileViewSet, basename='customer-profile')
router.register(r'wishlist', api_views.CustomerWishlistViewSet, basename='customer-wishlist')

urlpatterns = router.urls
