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
        "count_zzims",
    )

    filter_horizontal = ("zzim_list",)
