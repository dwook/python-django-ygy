from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # Custom Model

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
    phone = models.CharField(max_length=13, blank=True)

    def get_absolute_url(self):
        pass
