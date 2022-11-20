from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required # for function based views requires user to login with their credential
from django.contrib.auth.mixins import LoginRequiredMixin # For class based views requires user to login with their credential
from django.contrib import messages
from . import models
from userpreferences.models import UserPreference
from django.views import View
from django.contrib.auth.models import User
import datetime
from dateutil.relativedelta import relativedelta
from django.core.paginator import Paginator
import json
import csv
import xlwt
from django.template.loader import render_to_string
# from weasyprint import HTML
import tempfile
# from django.db.models import Sum



class IndexPageView(LoginRequiredMixin, View):
    login_url = '/authentication/login'
    def get(self, request):
        expenses = models.Expense.objects.filter(owner=request.user)
        paginator = Paginator(expenses, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        exist = UserPreference.objects.filter(user=request.user).exists()
        if not exist:
            UserPreference.objects.create(user=request.user, currency='CAD - Canadian Dollar')
        currency = UserPreference.objects.get(user=request.user).currency

        # import pdb
        # pdb.set_trace()
        context = {
            'expenses': expenses,
            'page_obj': page_obj,
            'currency': currency
        }
        # import pdb
        # pdb.set_trace()
        return render(request, 'expenses/index.html', context)

class AddExpenseView(LoginRequiredMixin, View):
    login_url = '/authentication/login'
    categories = models.Category.objects.all()


    def get(self, request):
        max_date = datetime.datetime.now().strftime ("%Y-%m-%d")
        context = {
            'categories': self.categories,
            'max_date': max_date,
        }
        return render(request, 'expenses/add_expense.html', context)
    
    def post(self, request):
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        expense_date = request.POST['expense_date']
        max_date = datetime.datetime.now().strftime ("%Y-%m-%d")
        context = {
            'categories': self.categories,
            'values': request.POST,
            'max_date': max_date,
        }

        # import pdb
        # pdb.set_trace()
         
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html', context)
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/add_expense.html', context)
        if category == "Choose...":
            messages.error(request, 'Category is required')
            return render(request, 'expenses/add_expense.html', context)
        if not expense_date:
            messages.error(request, 'Date is required')
            return render(request, 'expenses/add_expense.html', context)

        # import pdb
        # pdb.set_trace()

        models.Expense.objects.create(owner=request.user, amount=amount, description=description, category=category, date=expense_date)
        messages.success(request, "Expense saved successfully!")
        return redirect('expenses:expenses')
        
class EditExpenseView(LoginRequiredMixin, View):
    login_url = '/authentication/login'
    def get(self, request, id):
        expense = models.Expense.objects.get(pk=id)
        categories = models.Category.objects.all()
        new_date = expense.date.strftime("%Y-%m-%d")
        max_date = datetime.datetime.now().strftime("%Y-%m-%d")
        context = {
            'expense': expense,
            'categories': categories,
            'new_date': new_date,
            'max_date': max_date,
        }  
        # import pdb
        # pdb.set_trace()
        
        return render(request, 'expenses/edit_expense.html', context)

    def post(self, request, id):
        expense = models.Expense.objects.get(pk=id)
        categories = models.Category.objects.all()
        
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        expense_date = request.POST['expense_date']

        context = {
            'expense': expense,
            'categories': categories,
        }
        
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit_expense.html', context)
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/edit_expense.html', context)
        if category == "Choose..." and not category:
            messages.error(request, 'Category is required')
            return render(request, 'expenses/edit_expense.html', context)
        if not expense_date:
            messages.error(request, 'Date is required')
            return render(request, 'expenses/edit_expense.html', context)

        # import pdb
        # pdb.set_trace()

        expense.owner = request.user
        expense.amount = amount
        expense.description = description
        expense.category = category
        expense.date = expense_date
        expense.save()

        messages.success(request, 'Expenses updated successfully')
        return redirect('expenses:expenses')

class DeleteExpenseView(View):
    def get(self, request, id):
        expense = models.Expense.objects.get(pk=id)
        expense.delete()
        messages.success(request, 'Expense Removed')
        return redirect('expenses:expenses')

class SearchExpenseView(View):
    def post(self, request):
        search_str = json.loads(request.body).get('fieldValue', '')

        expenses = models.Expense.objects.filter(amount__istartswith=search_str, owner=request.user) | models.Expense.objects.filter(date__istartswith=search_str, owner=request.user) | models.Expense.objects.filter(description__icontains=search_str, owner=request.user) | models.Expense.objects.filter(category__icontains=search_str, owner=request.user)
        data = expenses.values()
        # print(list(data))
        return JsonResponse(list(data), safe=False)

class SummaryExpenseView(View):
    def get(self, request):
        return render(request, 'expenses/summary_expense.html')     


# https://djangodeconstructed.com/2020/01/03/mental-models-for-class-based-views/
def expense_category_summary(request):
    today = datetime.date.today()
    day_today = today.day - 1
    new_date = today - relativedelta(months=6)
    final_date = new_date - datetime.timedelta(days=day_today)
    expenses = models.Expense.objects.filter(owner=request.user, date__gte=final_date, date__lte=today)
    finalrep = {}

    def get_category(expense):
        return expense.category

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)
        
        for item in filtered_by_category:
            amount += item.amount

        return amount

    category_list = list(set(map(get_category, expenses)))
    print(category_list)

    for expense in expenses:
        for category in category_list:
            finalrep[category] = get_expense_category_amount(category)
    print(finalrep)
    return JsonResponse({'expense_category_data': finalrep}, safe=False)

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + str(datetime.datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['Category', 'Description', 'Amount', 'Date'])

    expenses = models.Expense.objects.filter(owner=request.user)

    for expense in expenses:
        writer.writerow([expense.category, expense.description, expense.amount, expense.date])

    return response


def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + str(datetime.datetime.now()) + '.xls'

    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('Expenses')
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    row_num = 0
    cols = ['Category', 'Description', 'Amount', 'Date']

    for col in range(len(cols)):
        worksheet.write(row_num, col, cols[col], font_style)

    font_style = xlwt.XFStyle()

    rows = models.Expense.objects.filter(owner=request.user).values_list('category', 'description', 'amount', 'date')

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            worksheet.write(row_num, col_num, str(row[col_num]), font_style)

    workbook.save(response)
    return response

# def export_pdf(request):
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename=Expenses' + str(datetime.datetime.now()) + '.pdf'
#     response['Content-Transfer-Encoding'] = 'binary'

#     html_string = render_to_string('expenses/pdf_output.html', { 
#         'expenses': [], 
#         'total': 0 
#         }
#     )
#     html = HTML(string=html_string)
#     result = html.write_pdf()
    
#     with tempfile.NamedTemporaryFile(delete=True) as output:
#         output.write(result)
#         output.flush
#         output = open(output.name, 'rb')
#         response.write(output.read())

    # return response