from django.shortcuts import render, redirect
from django.views import View
from . import models
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from django.contrib import messages
from django.core.paginator import Paginator
from userpreferences.models import UserPreference
from sales.models import Sales
# Create your views here.

class IndexPageView(LoginRequiredMixin, View):
    login_url = '/authentication/login'
    def get(self, request):
        purchases = models.Purchase.objects.filter(owner=request.user)
        paginator = Paginator(purchases, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        exist = UserPreference.objects.filter(user=request.user).exists()
        if not exist:
            UserPreference.objects.create(user=request.user, currency='CAD - Canadian Dollar')
        currency = UserPreference.objects.get(user=request.user).currency

        context = {
            'purchases': purchases,
            'page_obj': page_obj,
            'currency': currency
        }

        return render(request, 'purchases/index.html', context)

class AddPurchaseView(LoginRequiredMixin, View):
    login_url = '/authentication/login'
    origins = models.Origin.objects.all()
    product_units = models.ProductUnit.objects.all()

    def get(self, request):
        max_date = datetime.datetime.now().strftime ("%Y-%m-%d")
        context = {
            'origins': self.origins,
            'product_units': self.product_units,
            'max_date': max_date,
        }
        
        return render(request, 'purchases/add_purchase.html', context)

    def post(self, request):
        product_name = request.POST['product_name']
        purchase_date = request.POST['purchase_date']
        details = request.POST['details']
        origin = request.POST['origin']
        quantity = request.POST['quantity']
        product_unit = request.POST['product_unit']
        unit_cost = request.POST['unit_cost']
        total_cost = request.POST['total_cost']
        max_date = datetime.datetime.now().strftime ("%Y-%m-%d")
        context = {
            'max_date': max_date,
        }


        if not product_name.strip():
            messages.error(request, 'Product Name is required')
            return render(request, 'purchases/add_purchase.html', context)
        if not purchase_date:
            messages.error(request, 'Date is required')
            return render(request, 'purchases/add_purchase.html', context)
        if not details:
            messages.error(request, 'Details are required')
            return render(request, 'purchases/add_purchase.html', context)
        if not origin:
            messages.error(request, 'Origin is required')
            return render(request, 'purchases/add_purchase.html', context)
        if not quantity:
            messages.error(request, 'Quantity is required')
            return render(request, 'purchases/add_purchase.html', context)
        if not product_unit:
            messages.error(request, 'Product Unit is required')
            return render(request, 'purchases/add_purchase.html', context)
        if not unit_cost:
            messages.error(request, 'Unit Cost is required')
            return render(request, 'purchases/add_purchase.html', context)
        if not total_cost:
            messages.error(request, 'Total Cost is required')
            return render(request, 'purchases/add_purchase.html', context)

        models.Purchase.objects.create(
            owner=request.user, 
            product_name=product_name, 
            purchase_date=purchase_date, 
            details=details, 
            origin=origin,
            purchase_quantity=quantity,
            product_unit=product_unit,
            unit_cost=unit_cost,
            total_cost=total_cost
        )
        messages.success(request, "Purchase added successfully!")
        return redirect('purchases:purchases')

def inventory_summary_view(request):
    sales = Sales.objects.all()