# Generated by Django 4.0 on 2022-11-07 03:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0003_rename_productname_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales',
            name='products',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sales.products'),
        ),
    ]
