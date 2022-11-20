from django.contrib import admin
from .models import Inventory, InventoryType, CurrentTotalInventory, InventoryTransactions,TransactionType

# Register your models here.
class CurrentInventoryAdmin(admin.ModelAdmin):
    list_display = ['update_date', 'product_name', 'current_inventory_quantity', 'product_unit', 'inv_type', 'owner']

class InventoryAdmin(admin.ModelAdmin):
    list_display = ['date', 'product_name', 'inv_quantity', 'product_unit', 'inv_type', 'owner']

class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ['date', 'customer_supplier', 'product_name', 'quantity', 'product_unit', 'current_inventory', 'owner']


admin.site.register(Inventory, InventoryAdmin)
admin.site.register(InventoryType)
admin.site.register(InventoryTransactions, InventoryTransactionAdmin)
admin.site.register(TransactionType)
admin.site.register(CurrentTotalInventory, CurrentInventoryAdmin)
