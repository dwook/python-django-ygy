from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from common import models as common_models


class Review(common_models.TimeStampedModel):

    review = models.TextField()
    taste = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    quantity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    delivery = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    user = models.OneToOneField(
        "users.User", related_name="zzims", on_delete=models.CASCADE
    )
    restaurant = models.ManyToManyField(
        "restaurants.Restaurant", related_name="zzims", blank=True
    )

    def __str__(self):
        return f"{self.review} - {self.restaurant}"

    class Meta:
        ordering = ("-created",)
