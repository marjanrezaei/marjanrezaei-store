from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import ProductModel, ProductImageModel, ProductCategoryModel, WishlistProductModel
from django.utils.html import format_html
from dashboard.admin.forms import ProductForm


class ProductImageInline(admin.TabularInline):
    model = ProductImageModel
    extra = 1
    readonly_fields = ('file_preview',)
    fields = ('file', 'url', 'file_preview',)

    def file_preview(self, obj):
        if obj.url:
            return format_html('<img src="{}" style="max-height:100px"/>', obj.url)
        return "-"
    file_preview.short_description = "Preview"

@admin.register(ProductModel)
class ProductAdmin(TranslatableAdmin):
    form = ProductForm
    list_display = ("id", "title", "user", "stock", "price", "discount_percent", "status", "created_at", "image_preview")
    search_fields = ("translations__title", "translations__description")
    list_filter = ("status",)
    readonly_fields = ('image_preview',)
    inlines = [ProductImageInline]

    fieldsets = (
        (None, {
            'fields': ('user', 'category', 'title', 'slug', 'image', 'image_url',
                       'description', 'breif_description', 'stock', 'status',
                       'price', 'discount_percent')
        }),
    )

    def image_preview(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" style="max-height:100px"/>', obj.image_url)
        return "-"
    image_preview.short_description = "Main Image Preview"


@admin.register(ProductCategoryModel)
class ProductCategoryAdmin(TranslatableAdmin):
    list_display = ("id", "title", "created_at", "updated_at")
    search_fields = ("translations__title",)
    

@admin.register(WishlistProductModel)
class WishlistProductModelAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product")
