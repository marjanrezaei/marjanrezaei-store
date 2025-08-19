from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as drf_status
from django.shortcuts import get_object_or_404

from payment.models import PaymentModel, PaymentStatusType
from order.models import OrderStatusType
from payment.zarinpal_client import ZarinPalSandbox
from .serializers import PaymentSerializer, OrderSerializer


class PaymentVerifyAPIView(APIView):
    """
    API endpoint for verifying payments via ZarinPal.
    """

    SUCCESS_STATUSES = [100, 101]

    def get(self, request, *args, **kwargs):
        authority_id = request.query_params.get("authority")
        status = request.query_params.get("status")

        if not authority_id or not status:
            return Response(
                {"detail": "authority and status parameters are required"},
                status=drf_status.HTTP_400_BAD_REQUEST
            )

        payment = get_object_or_404(PaymentModel, authority_id=authority_id)
        order = getattr(payment, "order", None)

        if not order:
            return Response(
                {"detail": "Order not found for this payment"},
                status=drf_status.HTTP_404_NOT_FOUND
            )

        zarinpal = ZarinPalSandbox()
        try:
            response = zarinpal.payment_verify(int(payment.amount), payment.authority_id)
        except Exception:
            return Response(
                {"detail": "خطا در ارتباط با درگاه پرداخت. لطفاً دوباره تلاش کنید."},
                status=drf_status.HTTP_502_BAD_GATEWAY
            )

        is_success = response.get("status") in self.SUCCESS_STATUSES

        # Update payment
        payment.ref_id = response.get("RefID")
        payment.response_code = response.get("status")
        payment.response_json = response
        payment.status = PaymentStatusType.success.value if is_success else PaymentStatusType.failed.value
        payment.save()

        # Update order
        order.status = OrderStatusType.SUCCESS.value if is_success else OrderStatusType.FAILED.value
        order.save()

        payment_data = PaymentSerializer(payment, context={"request": request}).data
        order_data = OrderSerializer(order, context={"request": request}).data

        return Response({
            "payment": payment_data,
            "order": order_data,
            "is_success": is_success
        }, status=drf_status.HTTP_200_OK if is_success else drf_status.HTTP_400_BAD_REQUEST)
