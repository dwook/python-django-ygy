from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    fieldsets = (
        (
            "Custom Profile",
            {"fields": ("email", "nickname", "phone", "login_method", "is_owner",)},
        ),
    )

    list_display = (
        "email",
        "nickname",
        "phone",
        "login_method",
        "is_owner",
    )

    list_filter = ("is_owner",)
