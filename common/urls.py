from django.urls import path
from . import views

app_name = "common"


urlpatterns = [
    path("", views.home_view, name="home"),
    path("home/api/", views.home_view_api, name="home-api"),
    # path("home/api/", views.HomeApiView.as_view(), name="home-api"),
]
