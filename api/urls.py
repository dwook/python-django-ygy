from django.urls import path
from . import views


app_name = "api"

urlpatterns = [
    path("home/", views.HomeApi.as_view(), name="home-api"),
    path("groupbar/", views.GroupsBarApi.as_view(), name="groupbar-api"),
    path(
        "<int:group_id>/restaurants/",
        views.RestaurantsListApi.as_view(),
        name="restaurants-list-api",
    ),
    path(
        "restaurants/search/",
        views.SearchRestaurantsApi.as_view(),
        name="restaurants-search-api",
    ),
    path(
        "<int:restaurant_id>/restaurant-detail/",
        views.RestaurantDetailApi.as_view(),
        name="restaurant-detail-api",
    ),
    path(
        "<int:restaurant_id>/menus/",
        views.MenusListApi.as_view(),
        name="menus-list-api",
    ),
    path("zzims/", views.ZzimApi.as_view(), name="zzims-api",),
    path("orders/check/", views.OrderCheckApi.as_view(), name="order-check-api",),
    path("orders/add/", views.OrderAddApi.as_view(), name="order-add-api",),
    path("orders/", views.OrderListApi.as_view(), name="order-list-api",),
    path("orders/count/", views.OrderCountApi.as_view(), name="order-count-api",),
    path(
        "orders/delete/<int:menu_id>/",
        views.OrderDeleteApi.as_view(),
        name="order-delete-api",
    ),
    path(
        "orders/delete-all/",
        views.OrderDeleteAllApi.as_view(),
        name="order-delete-all-api",
    ),
]
