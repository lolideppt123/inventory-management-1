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
from decimal import Decimal, InvalidOperation
from django.utils.safestring import mark_safe
import json
from django.http import JsonResponse
from django.db.models import Q
from .serializers import SalesSerializer

class IndexPageView(LoginRequiredMixin, View):
    login_url = '/authentication/login'
    def get(self, request):
        sales = Sales.objects.filter(owner=request.user)
        paginator = Paginator(sales, 15)
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
        inv_trans = InventoryTransactions.objects.all()
    
        delivery_receipt = request.POST['delivery_receipt']
        invoice = request.POST['invoice']
        sales_date = request.POST['sales_date']
        customer = Customer.objects.get(name=request.POST['customer'])
        product_name = Products.objects.get(name=request.POST['product_name'])
        sold_quantity = request.POST['sold_quantity']
        product_unit = ProductUnit.objects.get(name=request.POST['product_unit'])
        unit_price = request.POST['unit_price']
        total_price = request.POST['total_price']
        unit_cost = request.POST['unit_cost']
        total_cost = request.POST['total_cost']
        margin = Decimal(total_price) - Decimal(total_cost)

        context = {
            'values': request.POST,
            'max_date': self.max_date,
            'products': self.products,
            'customers': self.customers,
            'product_units': self.product_units,
            'item_unit': ProductUnit.objects.get(name=product_name.product_unit),
        }

        try:
            margin_percent = margin / Decimal(total_cost)
        except InvalidOperation:
            messages.error(request, mark_safe("Cannot have a <strong>ZERO</strong> as Quantity"))
            return render(request, 'sales/add_sales.html', context)

        if not customer or customer == "Choose..." or customer == "Choose":
            messages.error(request, 'Please choose a Customer')
            return render(request, 'sales/add_sales.html', context)
        if not product_name or product_name == "Choose..." or product_name == "Choose":
            messages.error(request, 'Please choose a Product')
            return render(request, 'sales/add_sales.html', context)

        #Check if the user picked the right product unit
        if product_name.product_unit != product_unit:
            product_unit = ProductUnit.objects.get(name=product_name.product_unit)
            messages.info(request, mark_safe(f"We have changed <strong>{product_name}</strong> unit to its appropriate unit: <strong>\"{product_unit}\"</strong>"))
        # Prevents the User to input sales before starting Inventory
        for inv in inv_trans[1:2]:
            if inv.date > datetime.datetime.strptime(sales_date, "%Y-%m-%d").date():
                messages.error(request, mark_safe(f"Cannot add Sales <strong>BEFORE</strong> beginning Inventory"))
                return render(request, 'sales/add_sales.html', context)

        try:
            # Change this to add inventory type
            current_inv_list = CurrentTotalInventory.objects.filter(
                owner=request.user, 
                product_name=Products.objects.get(name=product_name),
                inv_type=InventoryType.objects.get(name="Finished Goods")
            )
        except CurrentTotalInventory.DoesNotExist:
            messages.error(request, mark_safe(f"You currently don't have <strong>{product_name}</strong> in stock"))
            return render(request, 'sales/add_sales.html', context)

        qty_on_hand = 0
        for curr_inv in current_inv_list:
            qty_on_hand = curr_inv.current_inventory_quantity

        if qty_on_hand < Decimal(sold_quantity):
            messages.error(request, mark_safe(f'Not enough <strong>{product_name}</strong> in stock'))
            return render(request, 'sales/add_sales.html', context)

        new_inventory_quantity = qty_on_hand - Decimal(sold_quantity)
        today_date = datetime.date.today()

        obj, created = CurrentTotalInventory.objects.get_or_create(owner=request.user, product_name=product_name, inv_type=InventoryType.objects.get(name="Finished Goods"))
        obj.owner = request.user
        obj.update_date = today_date
        obj.date = sales_date
        obj.current_inventory_quantity = new_inventory_quantity
        obj.save()
        # Create Sales
        new_sales = Sales.objects.create(
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
            unit_cost=unit_cost,
            total_cost=total_cost,
            margin=margin,
            margin_percent=margin_percent,
        )
        # Create InventoryTransaction
        InventoryTransactions.objects.create(
            owner=request.user, 
            transaction_type = TransactionType.objects.get(name="Sales"),
            update_date = today_date,
            date=sales_date,
            customer_supplier=customer,
            product_name=product_name,
            quantity=sold_quantity,
            product_unit=product_unit,
            current_inventory=new_inventory_quantity,
            sales_pk = Sales.objects.get(pk=new_sales.pk)
        )
        # Code for forgot to entry on previous days.
        inv_trans = InventoryTransactions.objects.filter(
            owner=request.user,
            product_name=product_name,
        )
        curr_inventory = 0
        for inv in inv_trans:
            obj = InventoryTransactions.objects.get(pk=inv.pk)
            if obj.transaction_type == TransactionType.objects.get(name="Inventory"):
                curr_inventory += inv.quantity
                obj.current_inventory = curr_inventory
            else:
                curr_inventory -= inv.quantity
                obj.current_inventory = curr_inventory
            obj.save()

        if request.POST['save'] == 'Save':
            messages.success(request, mark_safe(f"Sales of <strong>{product_name}</strong>, <strong>{sold_quantity} {product_unit}</strong> to <strong>{customer}</strong> has been saved successfully!"))
            return redirect('sales:sales')
        else:
            messages.success(request, mark_safe(f"Sales of <strong>{product_name}</strong>, <strong>{sold_quantity} {product_unit}</strong> to <strong>{customer}</strong> has been saved successfully!"))
            return redirect('sales:add_sales')

class EditSaleView(LoginRequiredMixin, View):
    login_url = '/authentication/login'
    products = Products.objects.all()
    customers = Customer.objects.all()
    product_units = ProductUnit.objects.all()

    max_date = datetime.datetime.now().strftime ("%Y-%m-%d")
    def get(self, request, id):
        sales = Sales.objects.get(pk=id)

        context = {
            'sales': sales,
            'values': request.GET,
            'products': self.products,
            'customers': self.customers,
            'product_units': self.product_units,
            'max_date': self.max_date,
        }

        return render(request, 'sales/edit_sales.html', context)

    def post(self, request, id):
        sales = Sales.objects.get(pk=id)
        inv_trans = InventoryTransactions.objects.all()
        current_total_inventory = CurrentTotalInventory.objects.all()
        today_date = datetime.date.today()
        
        delivery_receipt = request.POST['delivery_receipt']
        invoice = request.POST['invoice']
        sales_date = request.POST['sales_date']
        customer = Customer.objects.get(name=request.POST['customer'])
        product_name = Products.objects.get(name=request.POST['product_name'])
        sold_quantity = request.POST['sold_quantity']
        product_unit = ProductUnit.objects.get(name=request.POST['product_unit'])
        unit_price = request.POST['unit_price']
        total_price = request.POST['total_price']
        unit_cost = request.POST['unit_cost']
        total_cost = request.POST['total_cost']
        margin = Decimal(total_price) - Decimal(total_cost)
        margin_percent = margin / Decimal(total_cost)

        context = {
            'sales': sales,
            'values': request.POST,
            'max_date': self.max_date,
            'products': self.products,
            'customers': self.customers,
            'product_units': self.product_units,
            'item_unit': ProductUnit.objects.get(name=product_name.product_unit),
        }

        if not customer or customer == "Choose..." or customer == "Choose":
            messages.error(request, 'Please choose a Customer')

        #Check if the user picked the right product unit
        if product_name.product_unit != product_unit:
            product_unit = ProductUnit.objects.get(name=product_name.product_unit)
            messages.info(request, mark_safe(f"We have changed <strong>{product_name}</strong> unit to its appropriate unit: <strong>\"{product_unit}\"</strong>"))

        # Prevents the User to input sales before starting Inventory
        for inv in inv_trans[1:2]:
            if inv.date > datetime.datetime.strptime(sales_date, "%Y-%m-%d").date():
                messages.error(request, mark_safe(f"Cannot place Sales <strong>BEFORE</strong> beginning Inventory"))
                return render(request, 'sales/edit_sales.html', context)

        # updates sales not saved yet
        sales.owner=request.user
        sales.delivery_receipt=delivery_receipt
        sales.invoice=invoice
        sales.date=sales_date
        sales.customer=customer
        sales.product_name=product_name
        sales.sold_quantity=sold_quantity
        sales.product_unit=product_unit
        sales.unit_price=unit_price
        sales.total_price=total_price
        sales.unit_cost=unit_cost
        sales.total_cost=total_cost
        sales.margin=margin
        sales.margin_percent=margin_percent

        try:
            # Change this to add inventory type
            current_inv_list = CurrentTotalInventory.objects.filter(
                owner=request.user, 
                product_name=Products.objects.get(name=product_name),
                inv_type=InventoryType.objects.get(name="Finished Goods")
            )
        except CurrentTotalInventory.DoesNotExist:
            messages.error(request, mark_safe(f"You currently don't have <strong>{product_name}</strong> in stock"))
            return render(request, 'sales/edit_sales.html', context)

        qty_on_hand = 0
        for curr_inv in current_inv_list:
            qty_on_hand = curr_inv.current_inventory_quantity

        if qty_on_hand < Decimal(sold_quantity):
            messages.error(request, mark_safe(f'Not enough <strong>{product_name}</strong> in stock'))
            return render(request, 'sales/edit_sales.html/', context)

        # Saves sale
        sales.save()

        # Updates a specific InventoryTransaction
        inv_trans = InventoryTransactions.objects.get(sales_pk=sales)
        inv_trans.owner=request.user
        inv_trans.update_date=today_date
        inv_trans.date=sales_date
        inv_trans.customer_supplier=customer.name
        inv_trans.product_name=product_name
        inv_trans.quantity=sold_quantity
        inv_trans.product_unit=product_unit
        inv_trans.save()

        # Updates all InventoryTransaction and CurrentTotalInventory
        for item in current_total_inventory:
            curr_inventory = 0
            inv_trans = InventoryTransactions.objects.filter(owner=request.user, product_name=Products.objects.get(name=item.product_name))
            for inv in inv_trans:
                if inv.transaction_type == TransactionType.objects.get(name="Inventory"):
                    curr_inventory += inv.quantity
                    inv.current_inventory = curr_inventory
                    item.current_inventory_quantity = curr_inventory
                else:
                    curr_inventory -= inv.quantity
                    inv.current_inventory = curr_inventory
                    item.current_inventory_quantity = curr_inventory
                inv.save()
            item.save()

        if request.POST['save'] == 'Save':
            messages.success(request, mark_safe(f"Sales of <strong>{product_name}</strong>, <strong>{sold_quantity} {product_unit}</strong> to <strong>{customer}</strong> has been saved successfully!"))
            return redirect('sales:sales')

class SearchSalesView(LoginRequiredMixin,View):
    login_url = '/authentication/login'

    def post(self, request):
        search_str = json.loads(request.body).get('fieldValue', '')
        # https://stackoverflow.com/questions/41605962/how-to-use-incontains-for-filtering-by-using-foreignkey-in-django
        sales = Sales.objects.filter(
            Q(delivery_receipt__istartswith=search_str) |
            Q(invoice__istartswith=search_str) |
            Q(date__icontains=search_str) |
            Q(customer__name__istartswith=search_str) |
            Q(product_name__name__istartswith=search_str)
        )
        sales_serializer = SalesSerializer(sales, many=True)

        return JsonResponse(list(sales_serializer.data), safe=False)

class CsvImportForm(forms.Form):
    file = forms.FileField()

def productuploadcsv(request):
    if request.method == "POST":

        csv_file = request.FILES["file"]
        file_data = csv_file.read().decode("utf-8")
        csv_data = file_data.split("\n")

        # for Products
        for x in csv_data[1:-1]:
            data = x.split(",")
            data[1] = data[1].rstrip("\r")
            print(data)

            create = Products.objects.update_or_create(
                name=data[0],
                product_unit = ProductUnit.objects.get(name=data[1]),
            )
            product_list = Products.objects.all()
            print(product_list)
        ############################################

    form = CsvImportForm()
    context = {"form": form}
    return render(request, 'sales/product_upload.html', context)

def salesuploadcsv(request):
    if request.method == "POST":

        csv_file = request.FILES["file"]
        file_data = csv_file.read().decode("utf-8")
        csv_data = file_data.split("\n")

        # for Sales
        for data in csv_data[1:-1]:
            new_data = data.split(",")
            print(new_data)
            new_data[8] = new_data[8].rstrip("\r")

            print(new_data)

            create = Sales.objects.create(
                owner=request.user,
                delivery_receipt=new_data[0],
                invoice=new_data[1],
                sales_date=new_data[2],
                customer=Customer.objects.get(name=new_data[3]),
                product_name=Products.objects.get(name=new_data[4]),
                sold_quantity=new_data[5],
                product_unit=ProductUnit.objects.get(name=new_data[6]),
                unit_price=new_data[7],
                total_price=new_data[8]
            )
        ###############################################

    form = CsvImportForm()
    context = {"form": form}
    return render(request, 'sales/sales_upload.html', context)

def customeruploadcsv(request):
    
    if request.method == "POST":

        csv_file = request.FILES["file"]
        file_data = csv_file.read().decode("utf-8")
        csv_data = file_data.split("\n")

        # for Customers
        for x in csv_data[1:-1]:
            customer_list = x.rstrip("\r")
            create = Customer.objects.update_or_create(name=customer_list)
            print(customer_list)
        ###############################

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
        ###########################################



    form = CsvImportForm()
    context = {"form": form}
    return render(request, 'sales/customer_upload.html', context)

