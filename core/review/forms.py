from django import forms
from django.utils.translation import gettext_lazy as _

from .models import ReviewModel
from shop.models import ProductModel, ProductStatusType


class SubmitReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewModel
        fields = ['product', 'description', 'rate']
    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        
        try: 
            ProductModel.objects.get(id=product.id, status=ProductStatusType.publish.value)
        except ProductModel.DoesNotExist:
           raise forms.ValidationError(_("This product does not exist"))
        
        return cleaned_data