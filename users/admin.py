from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    fieldsets = (
        (
            "Custom Profile",
            {
                "fields": (
                    "username",
                    "email",
                    "phone",
                    "address",
                    "address_detail",
                    "login_method",
                    "is_owner",
                )
            },
        ),
    )

    list_display = (
        "username",
        "email",
        "phone",
        "login_method",
        "is_owner",
    )

    list_filter = ("is_owner",)
