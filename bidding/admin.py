from django.contrib import admin
from .models import Product, biddedAmount

admin.site.register([biddedAmount, Product])
