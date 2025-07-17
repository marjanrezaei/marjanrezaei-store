from django.forms import ModelForm, DateTimeInput
from order.models import CouponModel

class CouponForm(ModelForm):
    class Meta:
        model = CouponModel
        fields = [
            'code',
            'discount_percent',
            'max_limit_usage',
            'expiration_date',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['code'].widget.attrs['class'] = 'form-control'
        self.fields['discount_percent'].widget.attrs['class'] = 'form-control'
        self.fields['max_limit_usage'].widget.attrs['class'] = 'form-control'

        self.fields['expiration_date'].widget = DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }
        )

        