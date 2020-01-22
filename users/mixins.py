from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

# 로그인하지 않은 사람만(로그아웃한 사람만) 접근 가능
class LoggedOutOnlyView(UserPassesTestMixin):
    # https://docs.djangoproject.com/en/3.0/topics/auth/default/#django.contrib.auth.mixins.UserPassesTestMixin
    # test_func() 메서드에서 True를 리턴하면 다음 클래스를 사용할 수 있다.
    def test_func(self):
        return not self.request.user.is_authenticated  # 로그인한 사람이면 False 리턴

    # 로그인을 한 사람이 url을 직접 입력하여 접근했을 때 Home 화면으로 이동
    def handle_no_permission(self):
        # test_func()에서 False가 리턴되면 Home으로 이동
        return redirect("common:home")


# Email로 가입한 사람만 비밀번호 수정 페이지 접근 가능
# 네이버나 카카오로 로그인한 사용자들은 비밀번호 수정 페이지 접근 불가
class EmailLoginOnlyView(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.login_method == "email"

    def handle_no_permission(self):
        return redirect("common:home")


# 로그인한 사람만 접근 가능
class LoggedInOnlyView(LoginRequiredMixin):
    # 로그인하지 않은 사람(로그아웃한 사람)이 url을 직접 입력하여 접근했을 때 Login 화면으로 이동
    login_url = reverse_lazy("users:login")

