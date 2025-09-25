from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Avg
from django.utils.translation import gettext_lazy as _


class ReviewStatusType(models.IntegerChoices):
    pending = 1, _("Pending")
    accepted = 2,  _("Accepted")
    rejected = 3, _("Rejected")


class ReviewModel(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    product = models.ForeignKey('shop.ProductModel',on_delete=models.CASCADE)
    description = models.TextField()
    rate = models.IntegerField(default=5, validators=[
                               MinValueValidator(0), MaxValueValidator(5)])
    status = models.IntegerField(
        choices=ReviewStatusType.choices, default=ReviewStatusType.pending.value)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"{self.user} - {self.product.id}"
    
       
    def get_status(self):
        return {
            "id":self.status,
            "title":ReviewStatusType(self.status).name,
            "label":ReviewStatusType(self.status).label,
        }
        
        
@receiver(post_save, sender=ReviewModel)
def calculate_avg_review(sender, instance, **kwargs):
    product = instance.product
    accepted_reviews = ReviewModel.objects.filter(
        product=product,
        status=ReviewStatusType.accepted
    )
    avg_rating = accepted_reviews.aggregate(Avg("rate"))["rate__avg"] or 0
    product.avg_rate = round(avg_rating, 1)
    product.save()
