from django.db import models
from common import models as common_models


class Order(common_models.TimeStampedModel):
    name = models.ForeignKey(
        "users.User", related_name="orders", on_delete=models.CASCADE
    )
    menu = models.ForeignKey(
        "menus.Menu", related_name="orders", on_delete=models.CASCADE
    )
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.menu.name
