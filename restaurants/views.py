from django.views.generic import View
from django.http import JsonResponse
from django.shortcuts import render
from . import models, forms
import json


class RestaurantView(View):
    def get(self, request, *args, **kwargs):
        group_id = kwargs.get("group_id")

        return render(
            request, "restaurants/restaurants_list.html", {"group_id": group_id},
        )


class RestaurantsDetailView(View):
    def get(self, request, *args, **kwargs):
        restaurant_id = kwargs.get("restaurant_id")

        return render(
            request,
            "restaurants/restaurants_detail.html",
            {"restaurant_id": restaurant_id},
        )
