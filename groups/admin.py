from django.contrib import admin
from django.utils.html import mark_safe
from . import models


@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        # mark_safe는 장고한테 이 코드 또는 스크립트(html)는 안전한 것이라고 알려주는 것을 의미
        return mark_safe(f"<img src='{obj.photo.url}' width='50px' />")

    get_thumbnail.short_description = "Thumbnail"

