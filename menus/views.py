from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import render
from . import models
import json


def menus_list_view(request, restaurants_id, groups_id):
    return render(
        request,
        "menus/menus_list.html",
        {"restaurants_id": restaurants_id, "groups_id": groups_id},
    )

