from django.shortcuts import render
from django.views.generic import View, TemplateView
from groups import models as group_models


class HomeView(TemplateView):
    template_name = "home/home.html"

