from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import ProductModel, ProductImageModel, ProductCategoryModel, WishlistProductModel
from django.utils.html import format_html


@admin.register(ProductModel)
class ProductAdmin(TranslatableAdmin):
    list_display = ("id", "title", "stock", "price", "discount_percent", "status", "created_at", "image_preview")
    search_fields = ("translations__title", "translations__description")
    list_filter = ("status",)

    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image_url)
        return "-"
    image_preview.short_description = "Main Image Preview"


@admin.register(ProductImageModel)
class ProductImageModelAdmin(admin.ModelAdmin):
    list_display = ("id", "file_preview", "created_at")
    readonly_fields = ('file_preview',)

    def file_preview(self, obj):
        if obj.url:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.url)
        return "-"
    file_preview.short_description = "Extra Image Preview"


@admin.register(ProductCategoryModel)
class ProductCategoryAdmin(TranslatableAdmin):
    list_display = ("id", "title", "created_at")
    search_fields = ("translations__title",)


@admin.register(WishlistProductModel)
class WishlistProductModelAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product")
