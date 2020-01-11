from django.db import models
from common import models as common_models


class Restaurant(common_models.TimeStampedModel):
    group = models.ForeignKey("groups.Group", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
