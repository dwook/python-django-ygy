from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import render
from groups import models as group_models
from . import models
import json


def restaurants_list_view(request, groups_id):
    return render(
        request, "restaurants/restaurants_list.html", {"groups_id": groups_id}
    )


class GroupListApiView(View):
    def get(self, request, *args, **kwargs):
        groups = group_models.Group.objects.all().values("id", "name")
        json_data = {
            "groups": list(groups),
            "groups_id": kwargs.get("groups_id"),
        }
        return HttpResponse(json.dumps(json_data), content_type="application/json",)


class RestaurantsListApiView(View):
    def get(self, request, *args, **kwargs):
        restaurants = models.Restaurant.objects.filter(
            group=kwargs.get("groups_id")
        ).values("id", "name", "photo", "delivery_cost", "minimum_amount")
        # print(restaurants[0].get("payment_method"))
        json_data = {
            "restaurants": list(restaurants),
        }
        return HttpResponse(json.dumps(json_data), content_type="application/json",)
