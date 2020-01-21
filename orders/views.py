from django.shortcuts import render
from django.views.generic import TemplateView


class OrderListView(TemplateView):
    template_name = "orders/orders-list.html"
