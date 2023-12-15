"""Integrate DjangoUseEmailAsUsername with admin module."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUserModel


class BaseUserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "birth_date", "gender",
                                         "phone_number", "profile_img", "is_contestant")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )
    list_display = (
        "email", "first_name", "last_name", "birth_date", "gender", "phone_number", "is_staff", "is_contestant")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)


admin.site.register(CustomUserModel, BaseUserAdmin)
