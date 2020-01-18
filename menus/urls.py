from django.urls import path
from . import views

app_name = "menus"

urlpatterns = [
    path(
        "restaurants/<int:restaurants_id>/groups/<int:groups_id>/",
        views.menus_list_view,
        name="menus-list",
    ),
]
