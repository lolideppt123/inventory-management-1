from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from sales import models as sales_models

# Create your models here.
class Inventory(models.Model):
    date = models.DateField(default=now)
    product_name = models.ForeignKey(sales_models.Products, on_delete=models.SET_NULL, null=True)
    supplier = models.CharField(max_length=250, default="Supplier")
    inv_quantity = models.DecimalField(decimal_places=2, max_digits=8)
    product_unit = models.ForeignKey(sales_models.ProductUnit, on_delete=models.SET_NULL, null=True)
    inv_type = models.ForeignKey('InventoryType', on_delete=models.SET_NULL, null=True)
    # current_inventory = models.DecimalField(decimal_places=2, max_digits=8, null=True)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)


    class Meta:
        verbose_name_plural = 'Inventories'

    def __str__(self):
        return str(self.product_name) or ""

class InventoryType(models.Model):
    name = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = 'Inventory Types'

    def __str__(self):
        return str(self.name) or ""

class CurrentTotalInventory(models.Model): # Try to get a date for last update_date
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    update_date = models.DateField(default=now, null=True)
    product_name = models.ForeignKey(sales_models.Products, on_delete=models.SET_NULL, null=True)
    current_inventory_quantity = models.DecimalField(decimal_places=2, max_digits=8, null=True)
    product_unit = models.ForeignKey(sales_models.ProductUnit, on_delete=models.SET_NULL, null=True)
    inv_type = models.ForeignKey('InventoryType', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = 'Current Total Inventories'

    def __str__(self):
        return str(self.product_name) or ""

class InventoryTransactions(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    transaction_type = models.ForeignKey('TransactionType', on_delete=models.SET_NULL, null=True)
    date = models.DateField(default=now, null=True)
    customer_supplier = models.CharField(max_length=250, null=False, verbose_name="Customer/Supplier")
    product_name = models.ForeignKey(sales_models.Products, on_delete=models.SET_NULL, null=True)
    quantity = models.DecimalField(decimal_places=2, max_digits=8)
    product_unit = models.ForeignKey(sales_models.ProductUnit, on_delete=models.SET_NULL, null=True)
    current_inventory = models.DecimalField(decimal_places=2, max_digits=10, null=True)

    class Meta:
        verbose_name_plural = 'Inventory Transactions'
        ordering = ['date']

    def __str__(self):
        return str(self.product_name) or ""

class TransactionType(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return str(self.name) or ""