from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from parler.models import TranslatableModel, TranslatedFields
from core.utils.liara_upload import upload_to_liara, delete_from_liara
from django.conf import settings
from django.utils.translation import get_language
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class ProductStatusType(models.IntegerChoices):
    publish = 1, ("Show")
    draft = 2, ("Hide")
    
    
class ProductCategoryModel(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=255),
        slug=models.SlugField(allow_unicode=True),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.safe_translation_getter("title", any_language=True)


class ProductModel(TranslatableModel):
    user = models.ForeignKey("accounts.User", on_delete=models.PROTECT)
    category = models.ManyToManyField("ProductCategoryModel")
    
    translations = TranslatedFields(
        title=models.CharField(max_length=255),
        slug=models.SlugField(allow_unicode=True),
        description=models.TextField(),
        breif_description=models.TextField(null=True, blank=True),
    )

    image = models.ImageField(default="/default/product-image.png", upload_to="product/img/")
    image_url = models.URLField(blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    status = models.IntegerField(choices=ProductStatusType.choices, default=ProductStatusType.draft.value)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=0)
    discount_percent = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    avg_rate = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            if settings.LIARA_UPLOAD_ENABLED:
                uploaded_url = upload_to_liara(self.image, f"product-main-{self.id}.jpg", folder="product/img")
                if uploaded_url:
                    self.image_url = uploaded_url
                    super().save(update_fields=['image_url'])
            else:  # Local
                if not self.image_url:
                    self.image_url = self.image.url
                    super().save(update_fields=['image_url'])

    def get_absolute_url(self):
        slug = self.safe_translation_getter("slug", any_language=True)
        if not slug:
            return reverse("shop:product-detail", kwargs={"slug": str(self.id)})
        return reverse("shop:product-detail", kwargs={"slug": slug})

class ProductImageModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name="extra_images")
    file = models.ImageField(upload_to="product/extra-img/", blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.file:
            if settings.LIARA_UPLOAD_ENABLED:
                uploaded_url = upload_to_liara(self.file, f"product-extra-{self.id}.jpg", folder="product/extra-img")
                if uploaded_url:
                    self.url = uploaded_url
                    super().save(update_fields=['url'])
            else:  # Local
                if not self.url:
                    self.url = self.file.url
                    super().save(update_fields=['url'])


class WishlistProductModel(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.PROTECT)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.safe_translation_getter("title", any_language=True)


@receiver(pre_delete, sender=ProductModel)
def delete_product_images(sender, instance, **kwargs):
    if hasattr(instance, 'delete_main_image'):
        instance.delete_main_image()
    for img in instance.extra_images.all():
        if hasattr(img, 'delete_image'):
            img.delete_image()
        img.delete()

