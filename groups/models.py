from django.db import models
from common import models as common_models


class Group(common_models.TimeStampedModel):
    name = models.CharField(
        verbose_name="Group Name", max_length=100
    )
    photo = models.ImageField(
        verbose_name="Group Photo", upload_to="group_photos"
    )  # Image 처리를 위해 pillow 설치 필요

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        pass
