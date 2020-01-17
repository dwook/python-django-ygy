from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse


class User(AbstractUser):
    # 필드 추가

    LOGIN_EMAIL = "email"
    LOGIN_KAKAO = "kakao"
    LOGIN_NAVER = "naver"

    LOGIN_METHODS = (
        (LOGIN_EMAIL, "email"),
        (LOGIN_NAVER, "naver"),
        (LOGIN_KAKAO, "kakao"),
    )

    is_owner = models.BooleanField(default=False)
    login_method = models.CharField(
        max_length=20, choices=LOGIN_METHODS, default=LOGIN_EMAIL,
    )
    nickname = models.CharField(verbose_name="닉네임", max_length=100, blank=True)
    phone = models.CharField(verbose_name="전화번호", max_length=13, blank=True)

    def get_absolute_url(self):
        return reverse("users:edit-profile", kwargs={"pk": self.pk})

