from rest_framework import serializers
from .models import Sales

class SalesSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product_name.name')
    customer = serializers.CharField(source='customer.name')
    product_unit = serializers.CharField(source='product_unit.name')
    class Meta:
        model = Sales
        fields = (
            'pk',
            'delivery_receipt',
            'invoice',
            'date',
            'customer',
            'product_name',
            'sold_quantity',
            'product_unit',
            'unit_price',
            'total_price',
            'unit_cost',
            'total_cost',
            'margin',
            'margin_percent',
        )