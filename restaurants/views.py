from django.views.generic import View, TemplateView
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from groups import models as group_models
from . import models, forms
import json


class RestaurantView(View):
    def get(self, request, *args, **kwargs):
        group_id = kwargs.get("group_id")

        return render(
            request, "restaurants/restaurants_list.html", {"group_id": group_id},
        )

    # template_name = "restaurants/restaurants_list.html"


"""
class RestaurantView(View):
    def get(self, request, *args, **kwargs):
        group_pk = kwargs.get("group_pk")
        groups = group_models.Group.objects.all()
        restaurants = models.Group.objects.all()

        return render(
            request,
            "restaurants/restaurants_list.html",
            {"group_pk": group_pk, "groups": groups, "restaurants": restaurants},
        )
"""


def restaurants_list_view(request, group_pk):
    return render(request, "restaurants/restaurants_list.html", {"group_pk": group_pk})


class RestaurantsListApiView(View):
    def get(self, request, *args, **kwargs):
        restaurants = models.Restaurant.objects.filter(
            group=kwargs.get("group_pk")
        ).values("pk", "name", "photo", "delivery_cost", "minimum_amount", "group__pk")
        json_data = {
            "restaurants": list(restaurants),
        }
        return HttpResponse(json.dumps(json_data), content_type="application/json",)


class SearchApiView(View):
    def get(self, request, *args, **kwargs):

        form = forms.SearchForm(request.GET)

        if form.is_valid():
            search = form.cleaned_data.get("search")

            search_items = models.Restaurant.objects.filter(
                name__icontains=search
            ).union(models.Restaurant.objects.filter(menus__name__icontains=search))

            search_list = []

            for item in search_items:
                search_list += {
                    "pk": item.pk,
                    "name": item.name,
                    "photo": item.photo,
                    "delivery_cost": item.delivery_cost,
                    "minimum_amount": item.minimum_amount,
                }

            json_data = {
                "search_list": list(search_list),
            }
            print(JsonResponse(data=json_data))
            return JsonResponse(data=json_data)
