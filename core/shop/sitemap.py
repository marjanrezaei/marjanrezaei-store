from django.contrib.sitemaps import Sitemap
from .models import ProductModel, ProductStatusType

class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return ProductModel.objects.filter(status=ProductStatusType.publish.value)

    def location(self, obj):
        return obj.get_absolute_url()