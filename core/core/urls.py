from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler500, handler404, handler403
from django.views.i18n import set_language
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.contrib.sitemaps.views import sitemap
from shop.sitemap import ProductSitemap
from website.sitemap import StaticViewSitemap

sitemaps = {
    'products': ProductSitemap,
    'static': StaticViewSitemap, 
}


schema_view = get_schema_view(
    openapi.Info(
        title="Marjan Rezaei Store API",
        default_version="v1",
        description="Comprehensive API documentation for MarjanRezaei Store project.\n"
                    "Includes user, admin, products, orders, wishlist, and profile endpoints.",
        contact=openapi.Contact(email="rezaei.marjann@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# ---------- Error handlers ----------
handler404 = 'django.views.defaults.page_not_found'
handler403 = 'django.views.defaults.permission_denied'
handler500 = 'django.views.defaults.server_error'

# ---------- URL Patterns ----------
urlpatterns = [
    path('admin/', admin.site.urls),

    # Change language
    path('set-language/', set_language, name='set_language'),


    # HTML views
    path('', include('website.urls')),
    path("shop/", include("shop.urls", namespace="shop")),
    path('accounts/', include('accounts.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
    path('payment/', include('payment.urls')),
    path('review/', include('review.urls')),
    path('dashboard/', include('dashboard.urls')),

    # API views
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path("api/website/", include("website.api_urls")),
    path("api/shop/", include("shop.api_urls", namespace="shop_api")),
    path("api/accounts/", include("accounts.api_urls", namespace="accounts_api")),
    path("api/cart/", include("cart.api_urls")),
    path("api/order/", include("order.api_urls")),
    path("api/payment/", include("payment.api_urls")),
    path("api/review/", include("review.api_urls")),

    # Dashboard APIs
    path('api/dashboard/admin/', include('dashboard.api_admin.api_urls')),
    path('api/dashboard/customer/', include('dashboard.api_customer.api_urls')),

    # Swagger
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]

# ---------- Static & Media Files ----------
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
