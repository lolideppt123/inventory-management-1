from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django import forms

# Create your models here.
class Purchase(models.Model):
    product_name = models.CharField(max_length=150)
    purchase_date = models.DateField(default=now, null=True, blank=True)
    details = models.TextField()

    ORIGINS = [('IM', 'Imported'), ('LOC', 'Local')]
    origin = models.CharField(max_length=250, choices=ORIGINS, blank=True)

    purchase_quantity = models.DecimalField(decimal_places=2, max_digits=8)

    PRODUCT_UNIT = [('KILOGRAM', 'kg'), ('PIECES', 'pcs')]
    product_unit = models.CharField(max_length=250, choices=PRODUCT_UNIT, blank=True)
    unit_cost = models.DecimalField(decimal_places=2, max_digits=15)
    total_cost = models.DecimalField(decimal_places=2, max_digits=15)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-purchase_date']

    def __str__(self):
        return self.product_name

class Origin(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class ProductUnit(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name