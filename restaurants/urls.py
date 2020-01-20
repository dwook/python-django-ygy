from django.urls import path
from . import views

app_name = "restaurants"

urlpatterns = [
    path("<int:restaurant_id>/", views.RestaurantsDetailView.as_view(), name="detail"),
]
