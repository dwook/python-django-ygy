from django.db import models
from common import models as common_models


class AbstractItem(common_models.TimeStampedModel):

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class PaymentMethod(AbstractItem):
    class Meta:
        verbose_name_plural = "Payment Methods"


class Restaurant(common_models.TimeStampedModel):

    PAYMENT_HERE = "here"
    PAYMENT_THERE = "there"
    PAYMENT_METHOD = (
        (PAYMENT_HERE, "here"),
        (PAYMENT_THERE, "there"),
    )

    name = models.CharField(max_length=100, verbose_name="Restaurant name")
    owner = models.ForeignKey(
        "users.User", related_name="restaurants", on_delete=models.CASCADE
    )
    owner_comment = models.TextField()
    group = models.ManyToManyField("groups.Group")
    payment_method = models.ManyToManyField(
        "PaymentMethod", related_name="restaurants", blank=True
    )
    delivery_cost = models.IntegerField(default=0)
    minimum_amount = models.IntegerField(default=0)
    start_time = models.TimeField()
    end_time = models.TimeField()
    photo = models.ImageField(
        verbose_name="Restaurant photo", upload_to="restaurant_photos"
    )  # Image 처리를 위해 pillow 설치 필요

    def __str__(self):
        return self.name
