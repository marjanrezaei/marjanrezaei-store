from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "is_superuser", "is_active", "is_verified")
    list_filter = ("email", "is_superuser", "is_active", "is_verified")
    search_fields = ("email",)
    ordering = ("email",)
    fieldsets = ( 
        (
            "Authentication",
            {
                "fields": ("email", "password"),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_verified",
                ),
            },
        ),
        (
            "grop permitions",
            {
                "fields": (
                    "groups",
                    "user_permissions", 
                    "type", 
                ),
            },
        ),
        (
            "Important dates",
            {
                "fields": ("last_login",),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_verified",
                    "type",
                ),
            }, 
        ),
    )

class CustomProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "first_name", "last_name")
    search_fields = ("user", "first_name", "last_name")
    
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, CustomProfileAdmin)
