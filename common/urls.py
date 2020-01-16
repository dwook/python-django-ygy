from django.urls import path
from . import views

app_name = "common"


urlpatterns = [
    path("", views.home_view, name="home"),
    path("api/home/", views.HomeApiView.as_view(), name="home-api"),
    # path("api/home/", views.home_view_api, name="home-api"),
]
