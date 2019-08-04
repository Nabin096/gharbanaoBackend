from django.db import models

from designers.models import Designers
from seller.models import Sellers


class VerifiedDesigners(models.Model):
    id = models.AutoField(primary_key=True)
    designer = models.OneToOneField(Designers, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)
    document = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.designer.name + ' ' + str(self.verified)


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.name


class Products(models.Model):
    productID = models.CharField(max_length=15)
    name = models.CharField(max_length=40, null=True)
    company = models.CharField(max_length=40, null=True)
    price =  models.DecimalField(max_digits=8, decimal_places=2, null=True)
    availability = models.BooleanField(default=True)
    seller = models.ForeignKey(Sellers, null=True, blank=True, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + ' ' + self.company


class Bills(models.Model):
    billID = models.CharField(max_length=15)
    designer = models.ForeignKey(Designers, null=True, blank=True, on_delete=models.CASCADE)
    transactionID = models.CharField(max_length=15)
    totalPrice = models.DecimalField(max_digits=8, decimal_places=2)
    discount = models.DecimalField(max_digits=8, decimal_places=2)
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.billID + ' ' + self.designer.name + ' ' + self.transactionID


class ShippingAddress(models.Model):
    designer = models.ForeignKey(Designers, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    firmname = models.CharField(max_length=50, null=True)
    number = models.PositiveIntegerField(null=True)
    city = models.CharField(max_length=30, null=True)
    state = models.CharField(max_length=30, null=True)
    address = models.CharField(max_length=500, null=True)
    pincode = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.name + ' ' + self.firmname + ' ' + self.pincode


class Purchases(models.Model):
    designer = models.ForeignKey(Designers, null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    totalPrice = models.DecimalField(max_digits=8, decimal_places=2)
    discount = models.DecimalField(max_digits=8, decimal_places=2)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    seller = models.ForeignKey(Sellers, null=True, blank=True, on_delete=models.CASCADE)
    bill = models.ForeignKey(Bills, null=True, blank=True, on_delete=models.CASCADE)
    shippingAddress = models.ForeignKey(ShippingAddress, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.designer.name + ' ' + self.product.name + ' ' + self.quantity + ' ' + self.seller.name + ' ' + self.amount
