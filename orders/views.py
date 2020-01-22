from django.shortcuts import render
from django.views.generic import TemplateView
from users.mixins import LoggedInOnlyView


class OrderListView(LoggedInOnlyView, TemplateView):
    template_name = "orders/orders-list.html"
