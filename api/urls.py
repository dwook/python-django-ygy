from django.urls import path
from . import views


app_name = "api"

urlpatterns = [
    path("home/", views.HomeApi.as_view(), name="home-api"),
    path("groups-bar/", views.GroupsBarApi.as_view(), name="groups-bar-api"),
    path(
        "<int:group_id>/restaurants-list/",
        views.RestaurantsListApi.as_view(),
        name="restaurants-list-api",
    ),
]
