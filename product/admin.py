from django.contrib import admin
from . import models

admin.site.register(models.Address_Category)
admin.site.register(models.Address)
admin.site.register(models.Coupon)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
admin.site.register(models.Payment)
admin.site.register(models.Product)
admin.site.register(models.Product_Category)