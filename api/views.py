from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.generic import View
from django.views.generic.list import BaseListView
from django.views.generic.edit import BaseCreateView
from django.forms import model_to_dict
import json
from groups.models import Group
from restaurants.models import Restaurant
from menus.models import Menu


@method_decorator(ensure_csrf_cookie, name="dispatch")
class HomeApi(BaseListView):
    model = Group

    def render_to_response(self, context, **response_kwargs):
        # values()는 테이블에서 가져온 레코드들을 dict형태로 만들어 줌
        groups = list(context["object_list"].values())
        # safe가 True이면 data에 dict형인 값만 가능.
        # 여기서는 list형태로 데이터를 응답해서 보내주기 때문에 False
        return JsonResponse(data=groups, safe=False)


@method_decorator(ensure_csrf_cookie, name="dispatch")
class GroupsBarApi(BaseListView):
    model = Group

    def render_to_response(self, context, **response_kwargs):
        groups = list(context["object_list"].values())
        return JsonResponse(data=groups, safe=False)


@method_decorator(ensure_csrf_cookie, name="dispatch")
class RestaurantsListApi(View):
    def get(self, request, *args, **kwargs):
        group_id = kwargs.get("group_id")
        restaurants = list(Restaurant.objects.filter(group=group_id).values())
        # print(str(Restaurant.objects.filter(group=group_id).values().query))
        return JsonResponse(data=restaurants, safe=False)


class SearchRestaurantsApi(View):
    def post(self, request, *args, **kwargs):
        name = json.loads(self.request.body).get("name")

        search_restaurants = Restaurant.objects.filter(name__icontains=name).union(
            Restaurant.objects.filter(menus__name__icontains=name)
        )
        # print(str(search_restaurants.query))
        restaurants = list(search_restaurants.values())

        return JsonResponse(data=restaurants, safe=False)


@method_decorator(ensure_csrf_cookie, name="dispatch")
class RestaurantDetailApi(View):
    def get(self, request, *args, **kwargs):
        restaurant_id = kwargs.get("restaurant_id")
        # print(Restaurant.objects.all().values())
        restaurant = list(
            Restaurant.objects.filter(id=restaurant_id).values(
                "name",
                "owner_comment",
                "delivery_cost",
                "minimum_amount",
                "start_time",
                "end_time",
                "photo",
            )
        )
        payment_method = list(
            Restaurant.objects.filter(id=restaurant_id).values("payment_method__name",)
        )
        json_data = {
            "restaurant": restaurant,
            "payment_method": payment_method,
        }
        # print(json_data)
        # print(str(Restaurant.objects.filter(id=restaurant_id).values().query))
        return JsonResponse(data=json_data, safe=False)


@method_decorator(ensure_csrf_cookie, name="dispatch")
class MenusListApi(View):
    def get(self, request, *args, **kwargs):
        restaurant_id = kwargs.get("restaurant_id")
        restaurant = list(Menu.objects.filter(restaurant=restaurant_id).values())

        # print(str(Restaurant.objects.filter(id=restaurant_id).values().query))
        return JsonResponse(data=restaurant, safe=False)

