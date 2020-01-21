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
                    "email",
                    "nickname",
                    "phone",
                    "login_method",
                    "is_owner",
                    "zzim_list",
                    "cart_list",
                )
            },
        ),
    )

    list_display = (
        "email",
        "nickname",
        "phone",
        "login_method",
        "is_owner",
        "count_zzims",
    )

    list_filter = ("is_owner",)

    filter_horizontal = (
        "zzim_list",
        "cart_list",
    )
