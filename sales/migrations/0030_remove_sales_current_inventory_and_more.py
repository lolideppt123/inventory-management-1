# Generated by Django 4.0 on 2022-11-16 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0029_sales_current_inventory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sales',
            name='current_inventory',
        ),
        migrations.AddField(
            model_name='sales',
            name='current_inventory',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
    ]