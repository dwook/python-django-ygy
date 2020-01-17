from django.urls import path
from . import views
from groups import views as group_views

app_name = "common"


urlpatterns = [
    path("", views.home_view, name="home"),
    path("home-api/", group_views.HomeApiView.as_view(), name="home-api"),
]
