from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Sales(models.Model):
    delivery_receipt = models.CharField(max_length=250, default="0000", null=True, blank=True)
    invoice = models.CharField(max_length=250, default="0000", null=True, blank=True)
    date = models.DateField(default=now, null=True, blank=True)
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True)
    product_name = models.ForeignKey('Products', on_delete=models.SET_NULL, null=True)
    sold_quantity = models.DecimalField(decimal_places=2, max_digits=8)
    product_unit = models.ForeignKey('ProductUnit', on_delete=models.SET_NULL, null=True)
    unit_price = models.DecimalField(decimal_places=2, max_digits=15)
    total_price = models.DecimalField(decimal_places=2, max_digits=15)
    sold_type = models.ForeignKey('SoldType', on_delete=models.SET_NULL, null=True)

    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Sales'

    def __str__(self):
        return str(self.product_name) or ""

class Customer(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return str(self.name) or ""

    class Meta:
        ordering = ['name']

class Products(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return str(self.name) or ""

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ['name']

class ProductUnit(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return str(self.name) or ""

class SoldType(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return str(self.name) or ""