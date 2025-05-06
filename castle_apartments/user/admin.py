# user/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Seller

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("full_name", "email", "profile_image_url")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Roles"), {"fields": ("is_seller",)}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "is_seller"),
        }),
    )
    list_display = ("username", "email", "is_staff", "is_seller")
    search_fields = ("username", "email", "full_name")
    ordering = ("username",)

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ("user", "type", "agency_address")
    search_fields = ("user__username", "agency_address", "bio")
