from django.db import models
from common import models as common_admin


class Zzim(common_admin.TimeStampedModel):

    name = models.CharField(verbose_name="Zzim List Name", max_length=100)
    user = models.OneToOneField(
        "users.User", related_name="zzims", on_delete=models.CASCADE
    )
    restaurant = models.ManyToManyField(
        "restaurants.Restaurant", related_name="zzims", blank=True
    )

    def __str__(self):
        return self.name

    def count_restaurants(self):
        return self.restaurants.count()

    count_restaurants.short_description = "Number Of Restaurants"
