from django.contrib import admin
from .models import Product, biddedAmount, pending_orders

admin.site.register([biddedAmount, Product, pending_orders])
