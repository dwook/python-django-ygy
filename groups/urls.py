from django.urls import path
from restaurants import views as restaurant_views

app_name = "groups"

urlpatterns = [
    path(
        "<int:group_id>/",
        restaurant_views.RestaurantView.as_view(),
        name="restaurants-list",
    ),
]

