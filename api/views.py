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
from users.models import User
from . import models


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
                "id",
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
        if request.user.zzim_list.filter(id=restaurant_id):
            zzim_flag = True
        else:
            zzim_flag = False
        # print(str(request.user.zzim_list.filter(id=restaurant_id).query))
        json_data = {
            "restaurant": restaurant,
            "payment_method": payment_method,
            "zzim_flag": zzim_flag,
        }
        # print(str(Restaurant.objects.filter(id=restaurant_id).values().query))
        return JsonResponse(data=json_data, safe=False)


@method_decorator(ensure_csrf_cookie, name="dispatch")
class MenusListApi(View):
    def get(self, request, *args, **kwargs):
        restaurant_id = kwargs.get("restaurant_id")
        restaurant = list(Menu.objects.filter(restaurant=restaurant_id).values())

        # print(str(Restaurant.objects.filter(id=restaurant_id).values().query))
        return JsonResponse(data=restaurant, safe=False)


class ZzimApi(View):
    def post(self, request, *args, **kwargs):
        restaurant_id = json.loads(self.request.body).get("restaurant_id")
        restaurant = Restaurant.objects.get_or_none(id=restaurant_id)

        if restaurant is not None:
            if request.user.zzim_list.filter(id=restaurant_id):
                request.user.zzim_list.remove(restaurant)
                zzim_flag = False
                return JsonResponse(data={"zzim_flag": zzim_flag})
            else:
                request.user.zzim_list.add(restaurant)
                zzim_flag = True
                return JsonResponse(data={"zzim_flag": zzim_flag})


class CartAddApi(View):
    def post(self, request, *args, **kwargs):
        menu_id = json.loads(self.request.body).get("menu_id")
        menu = Menu.objects.get_or_none(id=menu_id)
        cart_all = request.user.cart_list.all()
        if menu is not None:
            print(menu)

            request.user.cart_list.add(menu)
            print(cart_all)
            zzim_flag = True
            return JsonResponse(data={"zzim_flag": zzim_flag})

