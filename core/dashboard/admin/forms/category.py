from django import forms
from parler.forms import TranslatableModelForm
from shop.models import ProductCategoryModel

class CategoryForm(TranslatableModelForm):
    class Meta:
        model = ProductCategoryModel
        # Only fields that exist in translations go here
        fields = ['title', 'slug']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }
