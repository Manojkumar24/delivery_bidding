from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Product(models.Model):
    prod_name = models.CharField(max_length=150)
    prod_id = models.IntegerField()
    description = models.TextField(max_length=264, blank=True)
    weight = models.PositiveIntegerField(default=2)

    def __str__(self):
        return self.prod_name


class biddedAmount(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    days = models.PositiveIntegerField()
    cost = models.FloatField()

    class Meta:
        unique_together = ('name', 'product')

    def __str__(self):
        return self.name.username