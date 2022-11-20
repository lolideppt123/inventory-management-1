from django.shortcuts import render, redirect
import json
import datetime
from . import models
from django.views import View
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from userpreferences.models import UserPreference
from django.contrib.auth.mixins import LoginRequiredMixin
from userpreferences.models import UserPreference

# Create your views here.
class IndexPageView(LoginRequiredMixin, View):
    login_url = '/authentication/login'
    def get(self, request):
        incomes = models.Income.objects.filter(owner=request.user)
        paginator = Paginator(incomes, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        currency = UserPreference.objects.get(user=request.user).currency
        # import pdb
        # pdb.set_trace()
        context = {
            'incomes': incomes,
            'page_obj': page_obj,
            'currency': currency
        }

        return render(request, 'income/index.html', context)

class AddIncomeView(LoginRequiredMixin, View):
    login_url = '/authentication/login'
    sources = models.Source.objects.all()


    def get(self, request):
        max_date = datetime.datetime.now().strftime ("%Y-%m-%d")
        context = {
            'sources': self.sources,
            'max_date': max_date,
        }
        return render(request, 'income/add_income.html', context)
    
    def post(self, request):
        amount = request.POST['amount']
        description = request.POST['description']
        source = request.POST['source']
        income_date = request.POST['income_date']
        max_date = datetime.datetime.now().strftime ("%Y-%m-%d")
        context = {
            'sources': self.sources,
            'values': request.POST,
            'max_date': max_date,
        }

        # import pdb
        # pdb.set_trace()
         
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/add_income.html', context)
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'income/add_income.html', context)
        if source == "Choose...":
            messages.error(request, 'Category is required')
            return render(request, 'income/add_income.html', context)
        if not income_date:
            messages.error(request, 'Date is required')
            return render(request, 'income/add_income.html', context)

        models.Income.objects.create(owner=request.user, amount=amount, description=description, source=source, date=income_date)
        messages.success(request, "Income saved successfully!")
        return redirect('incomes:incomes')

class EditIncomeView(LoginRequiredMixin, View):

    def get(self, request, id):
        income = models.Income.objects.get(pk=id)
        sources = models.Source.objects.all()
        new_date = income.date.strftime("%Y-%m-%d")
        max_date = datetime.datetime.now().strftime ("%Y-%m-%d")
        context = {
            'income': income,
            'sources': sources,
            'new_date': new_date,
            'max_date': max_date,
        }  
        # import pdb
        # pdb.set_trace()
        
        return render(request, 'income/edit_income.html', context)

    def post(self, request, id):
        income = models.Income.objects.get(pk=id)
        sources = models.Source.objects.all()
        
        amount = request.POST['amount']
        description = request.POST['description']
        source = request.POST['source']
        income_date = request.POST['income_date']

        context = {
            'income': income,
            'sources': sources,
        }
        
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/edit_income.html', context)
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'income/edit_income.html', context)
        if source == "Choose..." and not source:
            messages.error(request, 'source is required')
            return render(request, 'income/edit_income.html', context)
        if not income_date:
            messages.error(request, 'Date is required')
            return render(request, 'income/edit_income.html', context)

        # import pdb
        # pdb.set_trace()

        income.owner = request.user
        income.amount = amount
        income.description = description
        income.source = source
        income.date = income_date
        income.save()

        messages.success(request, 'Incomes updated successfully')
        return redirect('incomes:incomes')

class DeleteIncomeView(View):
    def get(self, request, id):
        income = models.Income.objects.get(pk=id)
        income.delete()
        messages.success(request, 'Income Removed')
        return redirect('incomes:incomes')

class SearchIncomeView(View):
    def post(self, request):
        search_str = json.loads(request.body).get('fieldValue', '')

        income = models.Income.objects.filter(amount__istartswith=search_str, owner=request.user) | models.Income.objects.filter(date__istartswith=search_str, owner=request.user) | models.Income.objects.filter(description__icontains=search_str, owner=request.user) | models.Income.objects.filter(source__icontains=search_str, owner=request.user)
        data = income.values()
        print(data)
        return JsonResponse(list(data), safe=False)
