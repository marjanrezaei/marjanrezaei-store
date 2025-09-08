from rest_framework import serializers
from payment.models import PaymentModel
from order.models import OrderModel


class PaymentSerializer(serializers.ModelSerializer):
    status_display = serializers.SerializerMethodField()

    class Meta:
        model = PaymentModel
        fields = [
            "id",
            "authority_id",
            "ref_id",
            "amount",
            "status",
            "status_display",
            "response_code",
            "response_json",
            "created_at",
            "updated_at",
        ]

    def get_status_display(self, obj):
        return obj.get_status()


class OrderSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = OrderModel
        fields = ["id", "status", "status_display", "created_at", "updated_at"]
        ref_name = "PymentOrderSerializer"
