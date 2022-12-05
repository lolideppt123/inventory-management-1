from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from sales.models import Products, ProductUnit, Sales
from sales.serializers import SalesSerializer
from . import models
from .serializers import InventorySerializer, InventoryTransactionsSerializer
from django.contrib import messages
from django.core.paginator import Paginator
from decimal import Decimal
import json
from django.http import JsonResponse
from rest_framework.response import Response
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.

class IndexPageView(LoginRequiredMixin, View):
    login_url = '/authentication/login'
    def get(self, request):
        return render(request, 'inventory/index.html')


class FinishedGoodsView(LoginRequiredMixin, View):
    login_url = '/authentication/login'

    def get(self, request):
        current_inv = models.CurrentTotalInventory.objects.filter(owner=request.user, inv_type=models.InventoryType.objects.get(name="Finished Goods"))
        paginator = Paginator(current_inv, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        for inv in page_obj:
            inv.message = self.get_inventory_message(inv)

        context = {
            'page_obj': page_obj,
            'current_inv': current_inv,
        }

        return render(request, 'inventory/finished_goods.html', context)

    def get_inventory_message(self, model):
        quantity = model.current_inventory_quantity

        if quantity <=  25:
            message = "danger"
            return message
        if quantity <=  50:
            message = "warning"
            return message
        if quantity <=  75:
            message = "primary"
            return message
        if quantity >= 100:
            message = "success"
            return message

    def inventory_summary(self, request):
        inv_type = models.InventoryType.objects.get(name="Finished Goods")
        inv = models.Inventory.objects.filter(owner=request.user, inv_type=inv_type)
        today = datetime.date.today()
        total_quantity = {}
        

        def get_product_name(inventory):
            return inventory.product_name
            
        def get_inventory_quantity(product_name):
            quantity = 0
            filter_by_product_name = inv.filter(product_name=product_name)

            for item in filter_by_product_name:
                quantity += item.inv_quantity

            if quantity <  5:
                message = "danger"
                return [quantity, message]
            if quantity <  10:
                message = "warning"
                return [quantity, message]
            if quantity <  15:
                message = "primary"
                return [quantity, message]
            if quantity >= 15:
                message = "success"
                return [quantity, message]
            

        def get_product_unit(product_name):
            filter_by_product_name = inv.filter(product_name=product_name)
            for unit in filter_by_product_name:
                prod_unit = unit.product_unit
                inv_type = unit.inv_type
            return [prod_unit, inv_type]


        product_name_list = list(set(map(get_product_name, inv)))


        # print(product_name_list)
        i = 0
        for product_name in product_name_list:
            i += 1
            total_quantity['product_'+str(i)] = [today, product_name, get_inventory_quantity(product_name)[0], get_product_unit(product_name)[0], get_product_unit(product_name)[1], get_inventory_quantity(product_name)[1]]

        return total_quantity

class RawMaterialsView(LoginRequiredMixin, View):
    login_url = '/authentication/login'
    
    def get(self, request):
        # inventories = models.Inventory.objects.filter(owner=request.user, inv_type=models.InventoryType.objects.get(name="Raw Materials"))
        # paginator = Paginator(inventories, 10)
        # page_number = request.GET.get('page')
        # page_obj = paginator.get_page(page_number)

        # context = {
        #     "inventories": inventories,
        #     'page_obj': page_obj,
        # }

        return render(request, 'inventory/raw_materials.html')


class AddInventoryView(LoginRequiredMixin, View):
    login_url = '/authentication/login'
    max_date = datetime.datetime.now().strftime("%Y-%m-%d")
    products = Products.objects.all()
    product_units = ProductUnit.objects.all()
    inventory_type = models.InventoryType.objects.all()

    def get(self, request):
        context = {
            'max_date': self.max_date,
            'product_units': self.product_units,
            'products': self.products,
            'inventory_type': self.inventory_type,
        }
        return render(request, 'inventory/add_inventory.html', context)

    def post(self, request):
        product_name = Products.objects.get(name=request.POST['product_name'])
        supplier = request.POST['supplier']
        inv_quantity = request.POST['inv_quantity']
        product_unit = ProductUnit.objects.get(name=request.POST['product_unit'])
        inv_date = request.POST['inv_date']
        inv_type = models.InventoryType.objects.get(name=request.POST['inv_type'])
        today_date = datetime.date.today()

        context = {
            'values': request.POST,
            'max_date': self.max_date,
            'inventory_type': self.inventory_type,
            'products': self.products,
            'product_units': self.product_units,
        }

        if inv_type.name == "Raw Materials":
            messages.error(request, 'Cannot add Raw Materials for now. Please try again later.')
            return render(request, 'inventory/add_inventory.html', context) 

        if not inv_date:
            messages.error(request, 'Date is required')
            return render(request, 'inventory/add_inventory.html', context) 

        if not product_name or product_name == "Choose..." or product_name == "Choose":
            messages.error(request, 'Please choose a Product')
            return render(request, 'inventory/add_inventory.html', context)

        if not inv_quantity:
            messages.error(request, 'Quantity is required')
            return render(request, 'inventory/add_inventory.html', context)

        if not product_unit:
            messages.error(request, 'Product Unit is required')
            return render(request, 'inventory/add_inventory.html', context)

        if not inv_type:
            messages.error(request, 'Product Unit is required')
            return render(request, 'inventory/add_inventory.html', context)
        #Check if the user picked the right product unit
        if product_name.product_unit != product_unit:
            product_unit = ProductUnit.objects.get(name=product_name.product_unit)
            messages.info(request, f"We have changed {product_name} unit to its appropriate unit: \"{product_unit}\"")
            print(product_unit)

        # Updates model
        try:
            inv = models.CurrentTotalInventory.objects.get(owner=request.user, product_name=product_name, inv_type=inv_type)
            current_inv = inv.current_inventory_quantity
            current_inventory_quantity = current_inv + Decimal(inv_quantity)
        except models.CurrentTotalInventory.DoesNotExist:
            current_inventory_quantity = Decimal(inv_quantity)

        obj, created = models.CurrentTotalInventory.objects.get_or_create(owner=request.user, product_name=product_name, inv_type=inv_type)
        obj.owner = request.user
        obj.update_date = today_date
        obj.date = inv_date
        obj.product_name = product_name
        obj.current_inventory_quantity = current_inventory_quantity
        obj.product_unit = product_unit
        obj.inv_type = inv_type
        obj.save()

        new_inventory = models.Inventory.objects.create(
            owner = request.user,
            supplier = supplier,
            product_name = product_name,
            product_unit = product_unit,
            date = inv_date,
            inv_quantity = inv_quantity,
            inv_type = inv_type,
        )

        if inv_type.name == "Finished Goods":
            new_transaction = models.InventoryTransactions.objects.create(
                owner=request.user, 
                transaction_type = models.TransactionType.objects.get(name="Inventory"),
                update_date = today_date,
                date=inv_date,
                customer_supplier=supplier,
                product_name=product_name,
                quantity=inv_quantity,
                product_unit=product_unit,
                current_inventory=current_inventory_quantity,
                inventory_pk = models.Inventory.objects.get(pk=new_inventory.pk)
            )

            # Code for forgot to entry on previous days.
            inv_trans = models.InventoryTransactions.objects.filter(
                owner=request.user,
                product_name=product_name,
            )
            curr_inventory = 0
            for inv in inv_trans:
                obj = models.InventoryTransactions.objects.get(pk=inv.pk)
                if obj.transaction_type == models.TransactionType.objects.get(name="Inventory"):
                    curr_inventory += inv.quantity
                    obj.current_inventory = curr_inventory
                else:
                    curr_inventory -= inv.quantity
                    obj.current_inventory = curr_inventory
                obj.save()

        if request.POST['save'] == 'Save':
            if inv_type == 'Raw Materials':
                messages.success(request, "Raw Material saved successfully!")
                return redirect('inventory:raw_materials')
            else:
                messages.success(request, f"Successfully added {product_name} to inventory!")
                return redirect('inventory:finished_goods')
        else:
            messages.success(request, f"Successfully added {product_name} to inventory!")
            return redirect('inventory:add_inventory')
        

class InventoryHistoryView(LoginRequiredMixin, View):
    login_url = '/authentication/login'
    def get(self, request):
        product_list = Products.objects.all()

        context = {
            "product_list": product_list,
        }
        return render(request, 'inventory/inventory_history.html', context)

    def post(self, request):
        product_picked = json.loads(request.body).get('fieldValue', '')
        product_name = Products.objects.get(name=product_picked)

        inventory_transaction = models.InventoryTransactions.objects.filter(owner=request.user, product_name=product_name)
        inventory_transaction_serializer = InventoryTransactionsSerializer(inventory_transaction, many=True)

        print(inventory_transaction_serializer.data)


        return JsonResponse(list(inventory_transaction_serializer.data), safe=False)
  
