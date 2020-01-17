from django.db import models
from common import models as common_models


class Menu(common_models.TimeStampedModel):

    name = models.CharField(max_length=100, verbose_name="Menu name")
    description = models.TextField()
    price = models.IntegerField(default=0)
    restaurant = models.ForeignKey(
        "restaurants.Restaurant", related_name="menus", on_delete=models.CASCADE,
    )
    photo = models.ImageField(verbose_name="Menu photo", upload_to="menu_photos")

    def __str__(self):
        return self.name
