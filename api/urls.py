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
    path(
        "search-restaurants/",
        views.SearchRestaurantsApi.as_view(),
        name="search-restaurants-api",
    ),
    path(
        "<int:restaurant_id>/restaurant-detail-api/",
        views.RestaurantDetailApi.as_view(),
        name="restaurant-detail-api",
    ),
    path(
        "<int:restaurant_id>/menus-list-api/",
        views.MenusListApi.as_view(),
        name="menus-list-api",
    ),
    path("zzim-api/", views.ZzimApi.as_view(), name="zzim-api",),
    path("order-check-api/", views.OrderCheckApi.as_view(), name="order-check-api",),
    path("order-add-api/", views.OrderAddApi.as_view(), name="order-add-api",),
]
