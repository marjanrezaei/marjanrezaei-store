from django.views.generic import (
    TemplateView,
    FormView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from order.permissions import CustomerRequiredMixin
from django.urls import reverse_lazy
from order.models import UserAddressModel, OrderModel, OrderItemModel
from order.forms import CheckOutForm
from cart.models import CartModel


class OrderCheckOutView(LoginRequiredMixin, CustomerRequiredMixin, FormView):
    template_name = "order/checkout.html"
    form_class = CheckOutForm
    success_url = reverse_lazy('order:completed')
    
    def get_form_kwargs(self):
        kwargs = super(OrderCheckOutView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        address = cleaned_data['address_id']
        cart = CartModel.objects.get(user=self.request.user)
        cart_items = cart.items.all()
        order = OrderModel.objects.create(
            user = self.request.user,
            address = address.address,
            state = address.state,
            city = address.city,
            zip_code = address.zip_code,
        )
        for item in cart_items:
            OrderItemModel.objects.create(
                order = order,
                product = item.product,
                quantity = item.quantity,
                price = item.product.get_price(),
            )
        cart_items.delete()
        order.total_price = order.calculate_total_price() 
        order.save()
        # print(self.request.POST)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(self.request.POST)
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = CartModel.objects.get(user=self.request.user) 
        context["addresses"] = UserAddressModel.objects.filter(user=self.request.user)
        total_price = cart.calculate_total_price()
        context["total_price"] = total_price
        context["total_tax"] = round((total_price * 9)/100)
        return context
    
    

class OrderCompletedView(LoginRequiredMixin, CustomerRequiredMixin, TemplateView):
    template_name = "order/completed.html"