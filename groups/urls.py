from django.urls import path
from . import views
from restaurants import views as restaurant_views

app_name = "groups"

urlpatterns = [
    path("<int:group_pk>/", restaurant_views.restaurants_list_view, name="detail",),
    path(
        "<int:group_pk>/restaurants/",
        restaurant_views.restaurants_list_view,
        name="restaurants-list",
    ),
    path(
        "<int:group_pk>/restaurants/groups-list-api/",
        views.GroupListApiView.as_view(),
        name="groups-list-api",
    ),
    path(
        "<int:group_pk>/restaurants/restaurants-list-api/",
        restaurant_views.RestaurantsListApiView.as_view(),
        name="restaurants-list-api",
    ),
    path(
        "<int:group_pk>/restaurants/search-api/",
        restaurant_views.SearchApiView.as_view(),
        name="search-api",
    ),
]

