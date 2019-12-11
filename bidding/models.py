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
    pincode = models.PositiveIntegerField()

    class Meta:
        unique_together = ('product', 'name', 'pincode')

    def __str__(self):
        return self.name.username


class pending_orders(models.Model):
    product = models.CharField(max_length=150)
    address = models.CharField(max_length=150)
    pincode = models.PositiveIntegerField()
    phone_num = models.PositiveIntegerField()
    customer = models.CharField(max_length=150)
    name = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name.username