from django.contrib import admin
from . import models


@admin.register(models.Restaurant)
class RestaurantAdmin(admin.ModelAdmin):

    list_display = ("group", "name")
