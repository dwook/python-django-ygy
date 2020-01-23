import os
import requests
import uuid
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView, TemplateView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import authenticate, login, logout
from . import forms, models
from users.mixins import LoggedInOnlyView, LoggedOutOnlyView, EmailLoginOnlyView


class LoginView(LoggedOutOnlyView, FormView):
    template_name = "users/login.html"
    form_class = forms.LoginForm
    # reverse_lazy는 View를 호출했을 때, 바로가 아닌 필요할 때(이 경우는 성공했을 때) 실행되도록 함
    # success_url = reverse_lazy("common:home")
    # form_valid는 FormView의 메서드 중 하나로 form.is_valid()를 대체하는 것으로 보면 된다.
    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        next_page = self.request.GET.get("next")
        if next_page is not None:
            return next_page
        else:
            return reverse("common:home")


class SignUpView(LoggedOutOnlyView, FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("common:home")

    def form_valid(self, form):
        user = form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        nickname = form.cleaned_data.get("nickname")
        user.username = email
        user.email = email
        user.set_password(password)
        user.nickname = nickname
        user.save()

        user = authenticate(self.request, username=email, password=password)

        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


def log_out(request):
    logout(request)
    return redirect(reverse("common:home"))


def naver_login(request):
    if os.environ.get("DEBUG"):
        client_id = os.environ.get("NAVER_ID")
        redirect_uri = "http://127.0.0.1:8000/users/login/naver/callback"
    else:
        client_id = os.environ.get("AWS_NAVER_ID")
        redirect_uri = "http://yogiyo-clone.7k63qgizbq.ap-northeast-2.elasticbeanstalk.com/users/login/naver/callback"
    # crsf 방지를 위해 uuid로 state(상태 토큰값) 생성
    state = uuid.uuid4().hex[:20]
    # 네이버 ID로 로그인 인증 요청 API
    return redirect(
        f"https://nid.naver.com/oauth2.0/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&state={state}"
    )


class NaverException(Exception):
    pass


def naver_callback(request):
    try:
        if os.environ.get("DEBUG"):
            client_id = os.environ.get("NAVER_ID")
            client_secret = os.environ.get("NAVER_SECRET")
        else:
            client_id = os.environ.get("AWS_NAVER_ID")
            client_secret = os.environ.get("AWS_NAVER_SECRET")
        # code : 로그인 인증 요청 API 호출이 성공하면 리턴받는 인증 코드값
        code = request.GET.get("code")
        state = request.GET.get("state")
        # 접근 토큰 발급 API(출력 포맷은 json)
        naver_token = requests.post(
            f"https://nid.naver.com/oauth2.0/token?client_id={client_id}&client_secret={client_secret}&grant_type=authorization_code&state={state}&code={code}"
        )
        token_json = naver_token.json()
        error = token_json.get("error", None)
        if error is not None:
            raise NaverException("Can't get authorization code.")
        # 접근 토큰 얻기
        access_token = token_json.get("access_token")
        # Naver 회원 프로필 정보 조회 API(출력 포맷은 json)
        profile_request = requests.get(
            "https://openapi.naver.com/v1/nid/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        response = profile_json.get("response")
        email = response.get("email", None)
        if email is None:
            raise NaverException("Please also give me your email")
        nickname = response.get("name")
        # Naver 계정 정보로 회원가입
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_NAVER:
                raise NaverException(f"Please log in with: {user.login_method}")
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email,
                username=email,
                nickname=nickname,
                login_method=models.User.LOGIN_NAVER,
            )
            user.set_unusable_password()
            user.save()
        # Naver 계정으로 기 가입되었으면 로그인
        login(request, user)
        return redirect(reverse("common:home"))
    except NaverException:
        return redirect(reverse("users:login"))


def kakao_login(request):
    client_id = os.environ.get("KAKAO_ID")
    if os.environ.get("DEBUG"):
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
    else:
        redirect_uri = "http://yogiyo-clone.7k63qgizbq.ap-northeast-2.elasticbeanstalk.com/users/login/kakao/callback"
        # 카카오 ID로 로그인 인증 요청 API
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        client_id = os.environ.get("KAKAO_ID")
        if os.environ.get("DEBUG"):
            redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        else:
            redirect_uri = "http://yogiyo-clone.7k63qgizbq.ap-northeast-2.elasticbeanstalk.com/users/login/kakao/callback"
        # code : 로그인 인증 요청 API 호출이 성공하면 리턴받는 인증 코드값
        code = request.GET.get("code")
        # 접근 토큰 발급 API(출력 포맷은 json)
        kakao_token = requests.post(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )
        token_json = kakao_token.json()
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoException("Can't get authorization code.")
        # 접근 토큰 얻기
        access_token = token_json.get("access_token")
        # 카카오 회원 프로필 정보 조회 API(출력 포맷은 json)
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        kakao_account = profile_json.get("kakao_account")
        email = kakao_account.get("email", None)
        if email is None:
            raise KakaoException("Please also give me your email")
        properties = profile_json.get("properties")
        nickname = properties.get("nickname")
        # 카카오 계정 정보로 회원가입
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_KAKAO:
                raise KakaoException(f"Please log in with: {user.login_method}")
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email,
                username=email,
                nickname=nickname,
                login_method=models.User.LOGIN_KAKAO,
            )
            user.set_unusable_password()
            user.save()
        # 카카오 계정으로 기 가입되었으면 로그인
        login(request, user)
        return redirect(reverse("common:home"))
    except KakaoException:
        return redirect(reverse("users:login"))


class EditProfileView(LoggedInOnlyView, UpdateView):
    template_name = "users/edit_profile.html"
    model = models.User
    fields = ("nickname", "phone")

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["nickname"].widget.attrs = {"placeholder": "닉네임"}
        form.fields["phone"].widget.attrs = {"placeholder": "전화번호"}

        return form

    def get_success_url(self):
        return self.request.user.get_absolute_url()


class EditPasswordView(LoggedInOnlyView, EmailLoginOnlyView, PasswordChangeView):

    template_name = "users/edit_password.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {"placeholder": "현재 비밀번호"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "새로운 비밀번호"}
        form.fields["new_password2"].widget.attrs = {"placeholder": "새로운 비밀번호 재확인"}
        return form

    def get_success_url(self):
        return self.request.user.get_absolute_url()


class ZzimListView(LoggedInOnlyView, TemplateView):
    template_name = "users/zzims_list.html"
