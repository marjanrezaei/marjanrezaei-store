from django.db import models
from django.db.models import JSONField

class PaymentStatusType(models.IntegerChoices):
    pending = 1 , "در انتظار"
    success = 2 , "پرداخت موفق"
    failed = 3 , "پرداخت ناموفق"
    
class PaymentModel(models.Model):
    authority_id = models.CharField(max_length=255, null=False, blank=False)
    ref_id = models.BigIntegerField(null=True, blank=True)
    amount =  models.DecimalField(default=0, max_digits=10, decimal_places=0)
    response_json = JSONField(default=dict)
    response_code = models.IntegerField(null=True, blank=True)
    status = models.IntegerField(choices=PaymentStatusType.choices, default=PaymentStatusType.pending.value)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_status(self):
        return{
            "id":self.status,
            "title":PaymentStatusType(self.status).name,
            "label":PaymentStatusType(self.status).label,
        }