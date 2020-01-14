from django.contrib import admin
from . import models


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        "review",
        "user",
        "restaurant",
        "taste",
        "quantity",
        "delivery",
    )
