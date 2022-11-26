from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from django.contrib import messages
from django.core.paginator import Paginator
from userpreferences.models import UserPreference
from django import forms
from .models import Customer, Products, Sales, ProductUnit
from inventory.models import Inventory, InventoryType, CurrentTotalInventory, InventoryTransactions, TransactionType
from decimal import Decimal

class IndexPageView(LoginRequiredMixin, View):
    login_url = '/authentication/login'
    def get(self, request):
        sales = Sales.objects.filter(owner=request.user)
        paginator = Paginator(sales, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'sales': sales,
            'page_obj': page_obj,
        }

        return render(request, 'sales/index.html', context)

class AddSaleView(LoginRequiredMixin, View):
    login_url = '/authentication/login'
    products = Products.objects.all()
    customers = Customer.objects.all()
    product_units = ProductUnit.objects.all()
    max_date = datetime.datetime.now().strftime ("%Y-%m-%d")

    def get(self, request):
        context = {
            'max_date': self.max_date,
            'products': self.products,
            'customers': self.customers,
            'product_units': self.product_units,
        }

        return render(request, 'sales/add_sales.html', context)

    def post(self, request):
        delivery_receipt = request.POST['delivery_receipt']
        invoice = request.POST['invoice']
        sales_date = request.POST['sales_date']
        customer = Customer.objects.get(name=request.POST['customer'].rstrip("\n\r"))
        product_name = Products.objects.get(name=request.POST['product_name'].rstrip("\n\r"))
        sold_quantity = request.POST['sold_quantity']
        product_unit = ProductUnit.objects.get(name=request.POST['product_unit'])
        unit_price = request.POST['unit_price']
        total_price = request.POST['total_price']

        context = {
            'values': request.POST,
            'max_date': self.max_date,
            'products': self.products,
            'customers': self.customers,
            'product_units': self.product_units,
        }

        if not sales_date:
            messages.error(request, 'Date is required')
            return render(request, 'sales/add_sales.html', context)
        if not customer or customer == "Choose..." or customer == "Choose":
            messages.error(request, 'Please choose a Customer')
            return render(request, 'sales/add_sales.html', context)
        if not product_name or product_name == "Choose..." or product_name == "Choose":
            messages.error(request, 'Please choose a Product')
            return render(request, 'sales/add_sales.html', context)
        if not sold_quantity:
            messages.error(request, 'Quantity is required')
            return render(request, 'sales/add_sales.html', context)
        if not product_unit:
            messages.error(request, 'Product Unit is required')
            return render(request, 'sales/add_sales.html', context)
        if not unit_price:
            messages.error(request, 'Unit price is required')
            return render(request, 'sales/add_sales.html', context)
        if not total_price:
            messages.error(request, 'Total price is required')
            return render(request, 'sales/add_sales.html', context)


        try:
            # Change this to add inventory type
            current_inv_list = CurrentTotalInventory.objects.filter(
                owner=request.user, 
                product_name=Products.objects.get(name=product_name),
                inv_type=InventoryType.objects.get(name="Finished Goods")
            )
        except CurrentTotalInventory.DoesNotExist:
            messages.error(request, "We currently don't have this PRODUCT in our Inventory")
            return render(request, 'sales/add_sales.html', context)

        qty_on_hand = 0
        for curr_inv in current_inv_list:
            qty_on_hand = curr_inv.current_inventory_quantity

        if qty_on_hand < Decimal(sold_quantity):
            messages.error(request, 'Not enough Product on hand')
            return render(request, 'sales/add_sales.html', context)

        new_inventory_quantity = qty_on_hand - Decimal(sold_quantity)
        today_date = datetime.date.today()

        obj, created = CurrentTotalInventory.objects.get_or_create(owner=request.user, product_name=product_name, inv_type=InventoryType.objects.get(name="Finished Goods"))
        obj.owner = request.user
        obj.update_date = sales_date
        obj.current_inventory_quantity = new_inventory_quantity
        obj.save()

        # import pdb
        # pdb.set_trace()
        
        Sales.objects.create(
            owner=request.user, 
            delivery_receipt=delivery_receipt, 
            invoice=invoice,
            date=sales_date,
            customer=customer,
            product_name=product_name,
            sold_quantity=sold_quantity,
            product_unit=product_unit,
            unit_price=unit_price,
            total_price=total_price,
            # current_inventory=new_inventory_quantity
        )

        InventoryTransactions.objects.create(
            owner=request.user, 
            transaction_type = TransactionType.objects.get(name="Sales"),
            date=sales_date,
            customer_supplier=customer,
            product_name=product_name,
            quantity=sold_quantity,
            product_unit=product_unit,
            current_inventory=new_inventory_quantity
        )



        messages.success(request, "Sales saved successfully!")
        return redirect('sales:sales')

class CsvImportForm(forms.Form):
    file = forms.FileField()

def customeruploadcsv(request):
    
    if request.method == "POST":

        # import pdb
        # pdb.set_trace()
        

        csv_file = request.FILES["file"]
        file_data = csv_file.read().decode("utf-8")
        csv_data = file_data.split("\n")
        # datas = csv_data.split("\r")

        # # for Customers
        # for x in csv_data:
        #     customer_list = x.rstrip("\r")
        #     create = Customer.objects.update_or_create(name=customer_list)
        #     print(customer_list)

        # # for Products
        # for x in csv_data:
        #     product_list = x.rstrip("\r")
        #     create = Products.objects.update_or_create(name=product_list)
        #     print(product_list)
            
        # # for Sales
        # for data in csv_data[1:-1]:
        #     new_data = data.split(",")
        #     print(new_data)
        #     new_data[8] = new_data[8].rstrip("\r")

        #     print(new_data)

        #     create = Sales.objects.create(
        #         owner=request.user,
        #         delivery_receipt=new_data[0],
        #         invoice=new_data[1],
        #         sales_date=new_data[2],
        #         customer=Customer.objects.get(name=new_data[3]),
        #         product_name=Products.objects.get(name=new_data[4]),
        #         sold_quantity=new_data[5],
        #         product_unit=ProductUnit.objects.get(name=new_data[6]),
        #         unit_price=new_data[7],
        #         total_price=new_data[8]
        #     )

        # # For Add Inventory
        # from inventory import models

        # for data in csv_data[1:-1]:
        #     new_data = data.split(",")
        #     # print(new_data[0])
        #     # print(new_data[1])
        #     # print(new_data[2])
        #     # print(new_data[3])
        #     # print(new_data[4])
        #     new_data[4] = new_data[4].rstrip("\r")
        #     print(new_data)


        #     models.Inventory.objects.create(
        #         owner=request.user,
        #         product_name=Products.objects.get(name=new_data[1]),
        #         product_unit=ProductUnit.objects.get(name=new_data[3]),
        #         inv_date=new_data[0],
        #         inv_quantity=new_data[2],
        #         inv_type=models.InventoryType.objects.get(name=new_data[4]),
        #     )



        
        # import pdb
        # pdb.set_trace()


    form = CsvImportForm()
    context = {"form": form}
    return render(request, 'sales/customer_upload.html', context)

