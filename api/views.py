from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.generic import View
from django.views.generic.list import BaseListView
from django.views.generic.edit import BaseFormView, BaseCreateView
from django.forms import model_to_dict
import json
from groups.models import Group
from restaurants.models import Restaurant


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
    def get(self, *args, **kwargs):
        group_id = kwargs.get("group_id")
        restaurants = list(Restaurant.objects.filter(group=group_id).values())

        return JsonResponse(data=restaurants, safe=False)


class SearchRestaurantsApi(View):
    def post(self, *args, **kwargs):
        name = json.loads(self.request.body).get("name")

        search_restaurants = Restaurant.objects.filter(name__icontains=name).union(
            Restaurant.objects.filter(menus__name__icontains=name)
        )
        restaurants = list(search_restaurants.values())

        return JsonResponse(data=restaurants, safe=False)


class ApiTodoCV(BaseCreateView):
    model = Group
    fields = "__all__"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["data"] = json.loads(self.request.body)
        return kwargs
