# Generated by Django 4.0 on 2023-09-21 23:07

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0033_products_product_unit_sales_margin_and_more'),
        ('inventory', '0021_currenttotalinventory_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='currenttotalinventory',
            options={'ordering': ['-date'], 'verbose_name_plural': 'Current Total Inventories'},
        ),
        migrations.AddField(
            model_name='inventorytransactions',
            name='inventory_pk',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.inventory'),
        ),
        migrations.AddField(
            model_name='inventorytransactions',
            name='sales_pk',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sales.sales'),
        ),
        migrations.AddField(
            model_name='inventorytransactions',
            name='update_date',
            field=models.DateField(default=django.utils.timezone.now, null=True),
        ),
    ]
