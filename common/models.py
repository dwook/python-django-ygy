from django.db import models
from . import managers


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = managers.CustomModelManager()

    class Meta:
        # 추상모델
        # 다른 모델들의 코드에서만 사용되고 실제 TimeStampedModel이라는 DB는 생성하지 않는다는 의미
        abstract = True
