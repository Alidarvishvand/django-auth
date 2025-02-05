from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, OTP


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("id", "phone_number", "username", "email", "is_active", "is_staff")
    search_fields = ("phone_number", "username", "email")
    ordering = ("id",)

    fieldsets = (
        (None, {"fields": ("phone_number", "username", "email", "password")}),
        ("اطلاعات شخصی", {"fields": ("first_name", "last_name")}),
        ("دسترسی‌ها", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("تاریخ‌ها", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("phone_number", "username", "email", "password1", "password2", "is_active", "is_staff"),
        }),
    )

class OTPAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "otp_code", "created_at")
    search_fields = ("phone_number", "otp_code")
    list_filter = ("created_at",)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(OTP, OTPAdmin)
