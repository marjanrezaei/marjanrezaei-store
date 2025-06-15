from django.contrib import admin
from .models import NewsLetterModel, ContactModel

# Register your models here.
admin.site.register(NewsLetterModel)
admin.site.register(ContactModel)

