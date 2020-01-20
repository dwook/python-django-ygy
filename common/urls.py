from django.urls import path
from . import views
from groups import views as group_views

app_name = "common"


urlpatterns = [path("", views.HomeView.as_view(), name="home")]
