from django.utils.html import format_html
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session

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
            {"fields": ("email", "password")},
        ),
        (
            "Permissions",
            {"fields": ("is_staff", "is_active", "is_superuser", "is_verified")},
        ),
        (
            "Group permissions",
            {"fields": ("groups", "user_permissions", "type")},
        ),
        (
            "Important dates",
            {"fields": ("last_login",)},
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
    list_display = ("user", "first_name", "last_name", "image_preview")
    search_fields = ("user__email", "first_name", "last_name")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" style="max-height: 80px; border-radius: 50%;"/>', obj.image_url)
        return "-"
    image_preview.short_description = "Profile Image"


admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, CustomProfileAdmin)


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()

    list_display = ['session_key', '_session_data', 'expire_date']
    readonly_fields = ['_session_data']


admin.site.register(Session, SessionAdmin)
