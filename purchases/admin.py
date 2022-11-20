from django.contrib import admin
from .models import Purchase, Origin, ProductUnit

# Register your models here.
class PurchaseAdmin(admin.ModelAdmin):
    # https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display
    # https://stackoverflow.com/questions/16235201/list-display-how-to-display-value-from-choices
    def get_origin(self, obj):
        return obj.get_origin_display()

    get_origin.short_description = 'origin'

    list_display = ['product_name', 'purchase_date', 'details', 'get_origin', 'purchase_quantity', 'product_unit', 'unit_cost', 'total_cost', 'owner']
    # list_editable = 
    list_per_page = 5

admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Origin)
admin.site.register(ProductUnit)