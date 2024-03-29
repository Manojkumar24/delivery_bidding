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
    location = models.CharField(max_length=150)

    class Meta:
        unique_together = ('product', 'name', 'location')

    def __str__(self):
        return self.name.username


status_choice = (
    ('Order Received', 'Order Received'),
    ('Order Shipped', 'Order Shipped'),
    ('Out for delivery', 'Out for delivery'),
    ('Delivered', 'Delivered'),
)


class pending_orders(models.Model):
    product = models.CharField(max_length=150)
    order_id = models.CharField(max_length=100)
    address = models.CharField(max_length=150)
    pincode = models.PositiveIntegerField()
    phone_num = models.PositiveIntegerField()
    customer = models.CharField(max_length=150)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    mail = models.EmailField(max_length=150)
    status = models.CharField(max_length=100, choices=status_choice, default='Order Received')

    def __str__(self):
        return self.name.username