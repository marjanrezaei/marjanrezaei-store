from django import forms
from order.models import UserAddressModel, CouponModel
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CheckOutForm(forms.Form):
    address_id = forms.IntegerField(required=True, label=_("Address"))
    coupon = forms.CharField(required=False, label=_("Coupon"))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CheckOutForm, self).__init__(*args, **kwargs)

    def clean_address_id(self):
        address_id = self.cleaned_data['address_id']
        user = self.request.user
        try:
            address = UserAddressModel.objects.get(id=address_id, user=user)
        except UserAddressModel.DoesNotExist:
            raise forms.ValidationError(
                _("Invalid address for the requested user.")
            )
        return address

    def clean_coupon(self):
        code = self.cleaned_data.get('coupon')
        user = self.request.user

        if not code:
            return None  # No coupon provided, return None

        try:
            coupon = CouponModel.objects.get(code=code)
        except CouponModel.DoesNotExist:
            raise forms.ValidationError(
                _("Invalid coupon code.")
            )

        if coupon.used_by.count() >= coupon.max_limit_usage:
            raise forms.ValidationError(
                _("Coupon usage limit reached.")
            )

        if coupon.expiration_date and coupon.expiration_date < timezone.now():
            raise forms.ValidationError(
                _("Coupon has expired.")
            )

        if user in coupon.used_by.all():
            raise forms.ValidationError(
                _("You have already used this coupon.")
            )

        return coupon
