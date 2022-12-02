from django.contrib import admin
from .models import Sales, Customer, Products, ProductUnit

# Register your models here.
class SalesAdmin(admin.ModelAdmin):
    list_display = [
        "delivery_receipt",
        "invoice",
        "date",
        "customer",
        "product_name",
        "sold_quantity",
        "product_unit",
        "unit_price",
        "total_price"
    ]

class ProductsAdmin(admin.ModelAdmin):
    list_display = ["name", "product_unit"]

admin.site.register(Sales, SalesAdmin)
admin.site.register(Customer)
admin.site.register(Products, ProductsAdmin)
admin.site.register(ProductUnit)
