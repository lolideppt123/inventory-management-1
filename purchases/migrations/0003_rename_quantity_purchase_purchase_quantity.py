# Generated by Django 4.0 on 2022-11-07 03:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0002_alter_purchase_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchase',
            old_name='quantity',
            new_name='purchase_quantity',
        ),
    ]
