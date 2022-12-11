from rest_framework import serializers
from .models import Inventory, CurrentTotalInventory, InventoryTransactions

class InventorySerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product_name.name')
    product_unit = serializers.CharField(source='product_unit.name')
    class Meta:
        model = Inventory
        fields = (
            'date',
            'product_name',
            'inv_quantity',
            'product_unit',
            'current_inventory',
        )

class CurrentTotalInventorySerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product_name.name')
    class Meta:
        model = CurrentTotalInventory
        fields = (
            'update_date',
            'product_name',
            'current_inventory_quantity',
            'product_unit',
        )

class InventoryTransactionsSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product_name.name')
    product_unit = serializers.CharField(source='product_unit.name')
    transaction_type = serializers.CharField(source='transaction_type.name')
    class Meta:
        model = InventoryTransactions
        fields = (
            'update_date',
            'date',
            'transaction_type',
            'customer_supplier',
            'product_name',
            'quantity',
            'product_unit',
            'current_inventory',
            'sales_pk',
            'inventory_pk',
        )

