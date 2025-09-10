from django.contrib import admin
from .models import NewsLetterModel, ContactModel


@admin.register(ContactModel)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone_number', 'created_at']
    search_fields = ['first_name', 'last_name', 'email']
    list_filter = ['created_at']
    readonly_fields = ['created_at']

admin.site.register(NewsLetterModel)

