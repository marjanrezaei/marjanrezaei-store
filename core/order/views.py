from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserAddressModel
from .serializers import CheckoutSerializer, OrderSerializer
from order.permissions import CustomerRequiredMixin
from order.models import UserAddressModel


@login_required
def checkout_view(request):
    addresses = UserAddressModel.objects.filter(user=request.user)
    
    if request.method == "POST":
        serializer = CheckoutSerializer(data=request.POST, context={'request': request})
        if serializer.is_valid():
            address = serializer.validated_data['address_id']
            coupon = serializer.validated_data.get('coupon_code', None)

            # Create Order
            order_data = {
                "user": request.user,
                "address": address,
                "state": address.state,
                "city": address.city,
                "zip_code": address.zip_code,
                "coupon": coupon
            }
            order_serializer = OrderSerializer(data=order_data)
            if order_serializer.is_valid():
                order_serializer.save()
                return redirect('order:success')  # Redirect after successful checkout
        else:
            return render(request, 'order/checkout.html', {
                'addresses': addresses,
                'errors': serializer.errors
            })

    return render(request, 'order/checkout.html', {'addresses': addresses})

class OrderCompletedView(LoginRequiredMixin, CustomerRequiredMixin, TemplateView):
    template_name = "order/completed.html"


class OrderFailedView(LoginRequiredMixin, CustomerRequiredMixin, TemplateView):
    template_name = "order/failed.html"

