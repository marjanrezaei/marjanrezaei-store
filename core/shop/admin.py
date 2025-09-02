from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import ProductModel, ProductImageModel, ProductCategoryModel, WishlistProductModel


@admin.register(ProductModel)
class ProductAdmin(TranslatableAdmin):
    list_display = ("id", "title", "stock", "price", "discount_percent", "status", "created_at")
    search_fields = ("translations__title", "translations__description")
    list_filter = ("status",)


@admin.register(ProductImageModel)
class ProductImageModelAdmin(admin.ModelAdmin):
    list_display = ("id", "file", "created_at")


@admin.register(ProductCategoryModel)
class ProductCategoryAdmin(TranslatableAdmin):
    list_display = ("id", "title", "created_at")
    search_fields = ("translations__title",)


@admin.register(WishlistProductModel)
class WishlistProductModelAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product")
