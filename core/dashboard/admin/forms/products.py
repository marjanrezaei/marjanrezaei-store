from django import forms
from shop.models import ProductModel

class ProductForm(forms.ModelForm):
    extra_images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control'}),
        required=False,
        label="تصاویر اضافی"
    )

    class Meta:
        model = ProductModel
        fields = [
            'category',
            'title',
            'slug',
            'image',
            'image_url',
            'description',
            'breif_description',
            'stock',
            'status',
            'price',
            'discount_percent',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            widget_class = 'form-control' if field_name != 'status' else 'form-select'
            self.fields[field_name].widget.attrs['class'] = widget_class
        self.fields['stock'].widget.attrs['type'] = 'number'