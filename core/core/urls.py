from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler500, handler404, handler403


# Error handlers
handler404 = 'django.views.defaults.page_not_found'
handler403 = 'django.views.defaults.permission_denied'
handler500 = 'django.views.defaults.server_error'

# ---------- URL Patterns ----------
urlpatterns = [
    path('admin/', admin.site.urls),
    
    # HTML views
    path('', include('website.urls')),
    path("shop/", include("shop.urls", namespace="shop")),
    path('accounts/', include('accounts.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
    path('payment/', include('payment.urls')),
    path('review/', include('review.urls')),
    
    # API views
    path("api/website/", include("website.api_urls")),
    path("api/shop/", include("shop.api_urls", namespace="shop_api")),
    path("api/accounts/", include("accounts.api_urls", namespace="accounts_api")),
    path("api/cart/", include("cart.api_urls", namespace="cart_api")), 
    path("api/order/", include("order.api_urls")),
    path("api/payment/", include("payment.api_urls")),
    path("api/review/", include("review.api_urls")),
 


    
    
    path('dashboard/', include('dashboard.urls')),
  
    
    

    # Dashboard APIs
    path('dashboard/admin/', include('dashboard.admin.urls')),
    path('dashboard/customer/', include('dashboard.customer.urls')),
]

# ---------- Static & Media Files ----------
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
