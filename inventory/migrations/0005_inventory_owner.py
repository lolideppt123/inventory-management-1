# Generated by Django 4.0 on 2022-11-13 06:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('inventory', '0004_inventorytype_inventory_inv_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='owner',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
    ]
