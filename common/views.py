from django.core.serializers import serialize
from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render
from groups import models as group_models
import json


def home_view(request):
    return render(request, "home/home.html")


# FBV
def home_view_api(request):
    groups = group_models.Group.objects.all().values("pk", "name", "photo")
    json_data = {
        "groups": list(groups),
    }
    return HttpResponse(json.dumps(json_data), content_type="application/json",)


# CBV
"""
class HomeApiView(View):
    def get(self, request, *args, **kwargs):
        groups = group_models.Group.objects.all().values("pk", "name", "photo")
        json_data = {
            "groups": list(groups),
        }
        return HttpResponse(json.dumps(json_data), content_type="application/json",)
"""
