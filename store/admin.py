from django.contrib import admin
from .models import VerifiedDesigners, Products, Bills, Purchases, Category, ShippingAddress

admin.site.register(VerifiedDesigners)
admin.site.register(Products)
admin.site.register(Bills)
admin.site.register(ShippingAddress)
admin.site.register(Purchases)
admin.site.register(Category)
