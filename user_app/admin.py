from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUserModel


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Additional Info',
            {
                'fields': (
                    'profile_img',
                )
            }
        )
    )


admin.site.register(CustomUserModel, CustomUserAdmin)