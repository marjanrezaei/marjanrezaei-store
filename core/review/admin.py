from django.contrib import admin
from .models import ReviewModel


@admin.register(ReviewModel)
class ReviewModelAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "rate", "status", "created_at")
  