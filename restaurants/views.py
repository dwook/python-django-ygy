from django.views.generic import View
from django.shortcuts import render

from users.mixins import LoggedInOnlyView


class RestaurantView(LoggedInOnlyView, View):
    def get(self, request, *args, **kwargs):
        group_id = kwargs.get("group_id")

        return render(
            request, "restaurants/restaurants_list.html", {"group_id": group_id},
        )


class RestaurantsDetailView(LoggedInOnlyView, View):
    def get(self, request, *args, **kwargs):
        restaurant_id = kwargs.get("restaurant_id")

        return render(
            request,
            "restaurants/restaurants_detail.html",
            {"restaurant_id": restaurant_id},
        )
