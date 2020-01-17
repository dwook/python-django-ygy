from django.urls import path
from . import views

app_name = "restaurants"

urlpatterns = [
    path(
        "groups/<int:groups_id>/", views.restaurants_list_view, name="restaurants-list",
    ),
    path(
        "groups/<int:groups_id>/groups-list-api/",
        views.GroupListApiView.as_view(),
        name="groups-list-api",
    ),
    path(
        "groups/<int:groups_id>/restaurants-list-api/",
        views.RestaurantsListApiView.as_view(),
        name="restaurants-list-api",
    ),
]
