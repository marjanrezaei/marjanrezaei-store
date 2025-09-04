from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils.translation import get_language
from parler.models import TranslatableModel, TranslatedFields
from core.utils.liara_upload import upload_to_liara, delete_from_liara


class ProductStatusType(models.IntegerChoices):
    publish = 1, ("نمایش")
    draft = 2, ("عدم نمایش")


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
    category = models.ManyToManyField(ProductCategoryModel)

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

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.safe_translation_getter("title", any_language=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save first to get an ID
        # Upload main image to Liara if not uploaded yet
        if self.image and not self.image_url:
            uploaded_url = upload_to_liara(self.image, f"product-main-{self.id}.jpg", folder="product/img")
            if uploaded_url:
                self.image_url = uploaded_url
                super().save(update_fields=['image_url'])

    def get_price(self):
        discount_amount = self.price * Decimal(self.discount_percent / 100)
        final_price = self.price - discount_amount
        return round(final_price)

    def is_discounted(self):
        return self.discount_percent != 0

    def is_published(self):
        return self.status == ProductStatusType.publish.value

    def get_absolute_url(self):
        lang = get_language()
        slug = self.safe_translation_getter("slug", language_code=lang, any_language=True)
        if not slug:
            return reverse("shop:product-detail", kwargs={"slug": self.id})
        return reverse("shop:product-detail", kwargs={"slug": slug})

    def delete_main_image(self):
        if self.image_url:
            key = "/".join(self.image_url.split('/')[-2:])
            delete_from_liara(key)
            self.image_url = None
        if self.image:
            self.image.delete(save=False)
            self.image = None
        self.save()


class ProductImageModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name="extra_images")
    file = models.ImageField(upload_to="product/extra-img/", blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save first to get an ID
        # Upload extra image to Liara if not uploaded yet
        if self.file and not self.url:
            uploaded_url = upload_to_liara(self.file, f"product-extra-{self.id}.jpg", folder="product/extra-img")
            if uploaded_url:
                self.url = uploaded_url
                super().save(update_fields=['url'])

    def delete_image(self):
        if self.url:
            key = "/".join(self.url.split('/')[-2:])
            delete_from_liara(key)
        if self.file:
            self.file.delete(save=False)


class WishlistProductModel(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.PROTECT)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.safe_translation_getter("title", any_language=True)


@receiver(pre_delete, sender=ProductModel)
def delete_product_images(sender, instance, **kwargs):
    instance.delete_main_image()
    for img in instance.extra_images.all():
        img.delete_image()
        img.delete()
