from django.contrib import admin
from . import models


@admin.register(models.Zzim)
class ZzimAdmin(admin.ModelAdmin):

    list_display = ("__str__", "user", "count_restaurants")

