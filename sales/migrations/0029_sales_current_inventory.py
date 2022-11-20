# Generated by Django 4.0 on 2022-11-16 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0012_rename_inv_date_inventory_date'),
        ('sales', '0028_alter_sales_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales',
            name='current_inventory',
            field=models.ManyToManyField(to='inventory.CurrentTotalInventory'),
        ),
    ]
