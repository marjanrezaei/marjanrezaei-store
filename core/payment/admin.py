from django.contrib import admin
from .models import PaymentModel


@admin.register(PaymentModel)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "authority_id",
        "amount",
        "response_code",
        "status",
        "created_at"
    )