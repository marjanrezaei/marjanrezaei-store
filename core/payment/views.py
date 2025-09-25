from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.db import connection
from django.http import HttpResponseServerError, JsonResponse
from django.utils.translation import gettext_lazy as _

from .models import PaymentModel, PaymentStatusType
from .zarinpal_client import ZarinPalSandbox
from order.models import OrderModel, OrderStatusType


class PaymentVerifyView(View):
    SUCCESS_STATUSES = [100, 101]

    def get(self, request, *args, **kwargs):
        authority_id = request.GET.get("authority")
        status = request.GET.get("status")

        if not authority_id or not status:
            return redirect(reverse_lazy("order:failed"))

        payment = get_object_or_404(PaymentModel, authority_id=authority_id)
        order = getattr(payment, "order", None)

        if not order:
            return redirect(reverse_lazy("order:failed"))

        zarinpal = ZarinPalSandbox()
        try:
            response = zarinpal.payment_verify(int(payment.amount), payment.authority_id)
        except Exception as e:
            return HttpResponseServerError(_("Error connecting to the payment gateway. Please try again."))

        is_success = response.get("status") in self.SUCCESS_STATUSES

        payment.ref_id = response.get("RefID")
        payment.response_code = response.get("status")
        payment.response_json = response
        payment.status = PaymentStatusType.success.value if is_success else PaymentStatusType.failed.value
        payment.save()

        order.status = OrderStatusType.SUCCESS.value if is_success else OrderStatusType.FAILED.value
        order.save()

        return redirect(reverse_lazy("order:completed" if is_success else "order:failed"))
