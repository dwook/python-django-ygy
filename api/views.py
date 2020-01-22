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
from orders.models import Order
from . import models


""" Home """
# csrf_exempt : 임시로 CSRF 미체크
# name="dispatch" : 이름이 dispatch인 메서드를 사용하겠다는 의미
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
        """
        브라우져에서 POST로 받아온 값은 request.body로 들어가는데
        request.body 안 값의 형태는 dict이지만 실제론 문자열이다(예: '{"abc" : 123}' )
        그래서 문자열을 dict로 변환해주기 위해 json.loads 메서드를 사용한다.

        반대로 dict를 문자열로 바꿔주는 함수가 있는데 json.dumps이다.
        """
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


# 찜 등록 또는 삭제
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


# 기존 주문표에 등록되어 있는 메뉴의 음식점명이 새로 등록된 메뉴의 음식점명과 같은지 다른지 체크
class OrderCheckApi(View):
    def post(self, request, *args, **kwargs):
        # 브라우져에서 받아온 값
        menu_id = json.loads(self.request.body).get("menu_id")
        menu = Menu.objects.get_or_none(id=menu_id)
        order_flag = False

        if (
            Order.objects.filter(menu__restaurant=menu.restaurant)
            or Order.objects.count() == 0
        ):
            order_flag = True  # 기존 & 신규 주문한 메뉴의 음식점명이 같거나 주문표가 빈 경우
        else:
            order_flag = False  # 기존 & 신규 주문한 메뉴의 음식점명이 다른 경우

        return JsonResponse(data={"order_flag": order_flag})


class OrderAddApi(View):
    def post(self, request, *args, **kwargs):
        # 기존 & 신규 주문한 메뉴의 음식점명이 다른 경우 기존 주문표 전체 삭제
        delete_flag = json.loads(self.request.body).get("delete_flag")
        if delete_flag == "True":
            print("delete_flag")
            Order.objects.all().delete()
        # 주문표 등록
        menu_id = json.loads(self.request.body).get("menu_id")
        menu = Menu.objects.get_or_none(id=menu_id)
        order_flag = False  # 저장 성공 여부

        if menu is not None:
            if Order.objects.filter(menu_id=menu_id):
                order = Order.objects.get(menu=menu)
                order.count += 1
                order.save()
                order_flag = True
            else:
                # get_or_create로 그냥 값을 받으면 tuple로 값을 받아오기 때문에(예: (order, True))
                # 따로 변수를 만들어 값을 받아옴. 두 번째 값은 필요없어서 _ 로 무시
                order, _ = Order.objects.get_or_create(menu=menu)
                order.count = 1
                order.save()
                order_flag = True

        return JsonResponse(data={"order_flag": order_flag})


@method_decorator(ensure_csrf_cookie, name="dispatch")
class OrderListApi(View):
    def get(self, request, *args, **kwargs):
        orders = list(
            Order.objects.all().values(
                "menu__id",
                "menu__name",
                "menu__description",
                "menu__photo",
                "menu__price",
                "count",
            )
        )

        return JsonResponse(data=orders, safe=False)


class OrderCountApi(View):
    def post(self, request, *args, **kwargs):
        menu_id = json.loads(self.request.body).get("menu_id")
        count = json.loads(self.request.body).get("count")

        try:
            if type(int(count)) is int:

                if int(count) < 1 or int(count) > 100:
                    return JsonResponse(data={}, status=400)

                if Order.objects.filter(menu_id=menu_id):
                    order = Order.objects.get(menu_id=menu_id)
                    order.count = count
                    order.save()

                    return JsonResponse(data={})
        except ValueError:
            return JsonResponse(data={}, status=400)


class OrderCountApi(View):
    def post(self, request, *args, **kwargs):
        menu_id = json.loads(self.request.body).get("menu_id")
        count = json.loads(self.request.body).get("count")

        try:
            if type(int(count)) is int:

                if int(count) < 1 or int(count) > 100:
                    return JsonResponse(data={}, status=400)

                if Order.objects.filter(menu_id=menu_id):
                    order = Order.objects.get(menu_id=menu_id)
                    order.count = count
                    order.save()

                    return JsonResponse(data={})
        except ValueError:
            return JsonResponse(data={}, status=400)


class OrderDeleteApi(View):
    def delete(self, request, *args, **kwargs):
        menu_id = kwargs.get("menu_id")
        Order.objects.get(menu_id=menu_id).delete()

        orders = list(
            Order.objects.all().values(
                "menu__id",
                "menu__name",
                "menu__description",
                "menu__photo",
                "menu__price",
                "count",
            )
        )

        return JsonResponse(data=orders, safe=False)
