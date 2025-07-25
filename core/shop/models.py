from django.db import models 
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator


class ProductStatusType(models.IntegerChoices):
    publish = 1 ,("نمایش")
    draft = 2 ,("عدم نمایش")
    
class ProductCategoryModel(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True)
    # parent = models.ForeignKey('self',on_delete=models.SET_NULL, null=True, related_name="category_child")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
class ProductModel(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.PROTECT)
    category = models.ManyToManyField(ProductCategoryModel)
    # category = models.ForeignKey(ProductCategoryModel, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True)
    image = models.ImageField(default="/default/product-image.png", upload_to="product/img/")
    description = models.TextField()
    breif_description = models.TextField(null=True, blank=True)
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
        return self.title
    
    def get_price(self):
        discount_amount = self.price * Decimal(self.discount_percent / 100)
        final_price = self.price - discount_amount
        return round(final_price)
    
    def is_discounted(self):
        return self.discount_percent != 0
    
    def is_published(self):
        return self.status == ProductStatusType.publish.value
    
    
class ProductImageModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    file = models.ImageField(upload_to="product/extra-img/")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class WishlistProductModel(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.PROTECT)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.product.title

