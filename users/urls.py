from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.log_out, name="logout"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/naver/", views.naver_login, name="naver-login"),
    path("login/naver/callback/", views.naver_callback, name="naver-callback"),
    path("login/kakao/", views.kakao_login, name="kakao-login"),
    path("login/kakao/callback/", views.kakao_callback, name="kakao-callback"),
    path("<int:pk>/edit/", views.EditProfileView.as_view(), name="edit-profile"),
    path("edit-password/", views.EditPasswordView.as_view(), name="edit-password"),
    path("zzims-list/", views.ZzimListView.as_view(), name="zzims-list"),
]
