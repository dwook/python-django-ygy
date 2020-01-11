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

    is_owner = models.BooleanField(verbose_name="Is Owner", default=False)
    login_method = models.CharField(
        verbose_name="Login Method",
        max_length=20,
        choices=LOGIN_METHODS,
        default=LOGIN_EMAIL,
    )
    phone = models.CharField(verbose_name="Phone", max_length=13, blank=True)
    address = models.CharField(verbose_name="Address", max_length=100, blank=True)
    address_detail = models.CharField(
        verbose_name="Address Detail", max_length=100, blank=True
    )

    def get_absolute_url(self):
        pass
