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
    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE
    )
    restaurant = models.ForeignKey(
        "restaurants.Restaurant", related_name="reviews", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.review} - {self.restaurant}"

    class Meta:
        ordering = ("-created",)
