from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("orders-list/", views.OrderListView.as_view(), name="orders-list"),
]

