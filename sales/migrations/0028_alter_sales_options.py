# Generated by Django 4.0 on 2022-11-16 03:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0027_alter_sales_options_rename_sales_date_sales_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sales',
            options={'ordering': ['date'], 'verbose_name_plural': 'Sales'},
        ),
    ]
