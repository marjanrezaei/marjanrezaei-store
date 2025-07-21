from django.views.generic import TemplateView, FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.http import JsonResponse
from decimal import Decimal, ROUND_HALF_UP
from django.shortcuts import redirect
from django.contrib import messages

from order.permissions import CustomerRequiredMixin
from order.models import UserAddressModel, OrderModel, OrderItemModel, CouponModel
from order.forms import CheckOutForm
from cart.models import CartModel
from payment.zarinpal_client import ZarinPalSandbox
from payment.models import PaymentModel



class OrderCheckOutView(LoginRequiredMixin, CustomerRequiredMixin, FormView):
    template_name = "order/checkout.html"
    form_class = CheckOutForm
    success_url = reverse_lazy('order:completed')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        address = form.cleaned_data['address_id']
        coupon = form.cleaned_data.get('coupon')
        
        cart = CartModel.objects.get(user=user)
        order = self.create_order(user, address, coupon)
        self.create_order_items(order, cart)

        order.total_price = order.final_price_with_tax()
        order.save()

        if coupon:
            coupon.used_by.add(user)
            coupon.save()

        cart.items.all().delete()

        return super().form_valid(form)
        # return self.redirect_to_payment(order)

    # def redirect_to_payment(self, order):
    #     zarinpal = ZarinPalSandbox()
    #     response = zarinpal.payment_request(order.total_price)

    #     if response.get("data") and response["data"].get("code") == 100:
    #         authority = response["data"]["authority"]

    #         payment_obj = PaymentModel.objects.create(
    #             authority_id=authority,
    #             amount=order.total_price,
    #         )
    #         order.payment = payment_obj
    #         order.save()

    #         return redirect(zarinpal.generate_payment_url(authority))

    #     # If payment failed
    #     error_message = response.get("errors", {}).get("message", "خطا در اتصال به درگاه پرداخت")
    #     messages.error(self.request, error_message)
    #     return redirect("order:checkout")

    def form_invalid(self, form):
        print("Form errors:", form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['addresses'] = UserAddressModel.objects.filter(user=user)
        try:
            cart = CartModel.objects.get(user=user)
            total = sum(item.product.get_price() * item.quantity for item in cart.items.all())
            discount = Decimal('0')  # No coupon initially
            discounted = total
            tax = (discounted * Decimal('0.09')).quantize(Decimal('1'))
            final = discounted + tax

            context['total_price'] = total
            context['discounted_price'] = discounted
            context['total_tax'] = tax
            context['final_price_with_tax'] = final
        except CartModel.DoesNotExist:
            pass

        return context

    def create_order(self, user, address, coupon=None):
        return OrderModel.objects.create(
            user=user,
            address=address.address,
            state=address.state,
            city=address.city,
            zip_code=address.zip_code,
            coupon=coupon,
        )

    def create_order_items(self, order, cart):
        for item in cart.items.all():
            OrderItemModel.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.get_price(),
            )
            

class OrderCompletedView(LoginRequiredMixin, CustomerRequiredMixin, TemplateView):
    template_name = "order/completed.html"

class OrderFailedView(LoginRequiredMixin, CustomerRequiredMixin, TemplateView): 
    template_name = "order/failed.html"

class ValidateCouponView(LoginRequiredMixin, CustomerRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            code = request.POST.get("code")
            user = request.user
            coupon = CouponModel.objects.get(code=code)

            if coupon.used_by.count() >= coupon.max_limit_usage:
                return JsonResponse({"message": "محدودیت در تعداد استفاده"}, status=403)

            if coupon.expiration_date and coupon.expiration_date < timezone.now():
                return JsonResponse({"message": "کد تخفیف منقضی شده است"}, status=403)

            if user in coupon.used_by.all():
                return JsonResponse({"message": "این کد تخفیف قبلا توسط شما استفاده شده است"}, status=403)

            cart = CartModel.objects.get(user=user)

            total = sum(
                Decimal(item.product.get_price()) * item.quantity
                for item in cart.items.all()
            )

            discount_percent = Decimal(coupon.discount_percent) / Decimal('100')
            discount = (total * discount_percent).quantize(Decimal('1'), rounding=ROUND_HALF_UP)

            discounted = total - discount
            tax = (discounted * Decimal('0.09')).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
            final = discounted + tax

            return JsonResponse({
                "message": "کد تخفیف با موفقیت اعمال شد.",
                "total_price": str(total),
                "discounted_price": str(discounted),
                "total_tax": str(tax),
                "final_price_with_tax": str(final)
            }, status=200)

        except CouponModel.DoesNotExist:
            return JsonResponse({"message": "کد تخفیف یافت نشد"}, status=404)

        except CartModel.DoesNotExist:
            return JsonResponse({"message": "سبد خرید شما خالی است"}, status=400)

        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({"message": "خطایی در سرور رخ داده است."}, status=500)
