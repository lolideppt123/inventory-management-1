# Generated by Django 4.0 on 2022-11-17 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0032_remove_sales_current_inventory'),
        ('inventory', '0017_transactiontype_inventorytransactions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventory',
            name='current_inventory',
        ),
        migrations.AddField(
            model_name='inventorytransactions',
            name='product_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sales.products'),
        ),
        migrations.AddField(
            model_name='inventorytransactions',
            name='product_unit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sales.productunit'),
        ),
    ]
