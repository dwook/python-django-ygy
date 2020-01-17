from django.http import HttpResponse
from django.views.generic import View
from . import models
import json

# CBV
class HomeApiView(View):
    def get(self, request, *args, **kwargs):
        groups = models.Group.objects.all().values("id", "name", "photo")
        json_data = {
            "groups": list(groups),
        }
        return HttpResponse(json.dumps(json_data), content_type="application/json",)


# FBV
"""
def home_view_api(request):
    groups = group_models.Group.objects.all().values("id", "name", "photo")
    json_data = {
        "groups": list(groups),
    }
    return HttpResponse(json.dumps(json_data), content_type="application/json",)
"""

