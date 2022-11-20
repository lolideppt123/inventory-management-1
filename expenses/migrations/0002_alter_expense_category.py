# Generated by Django 4.0 on 2022-10-10 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='category',
            field=models.CharField(choices=[('INSURANCE', 'Car Insurance'), ('RENTAL', 'House Rental'), ('Food', (('GROCERY', 'Grocery'), ('ORDER', 'Order'))), ('LOAN', 'Car Loan')], max_length=250),
        ),
    ]
