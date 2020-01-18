from django.shortcuts import render
from django.views.generic import View
from groups import models as group_models


class HomeView(View):
    def get(self, *args, **kwargs):
        groups = group_models.Group.objects.all()
        common_group_pk = group_models.Group.objects.filter(name="전체보기")
        return render(
            self.request,
            "home/home.html",
            {"groups": groups, "common_group": common_group_pk},
        )

