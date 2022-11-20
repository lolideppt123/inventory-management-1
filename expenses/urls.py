from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'expenses'

urlpatterns = [
    path('', views.IndexPageView.as_view(), name='expenses'),
    path('add_expense', views.AddExpenseView.as_view(), name='add_expense'),
    path('edit-expense/<id>', views.EditExpenseView.as_view(), name='edit_expense'),
    path('delete-expense/<id>', views.DeleteExpenseView.as_view(), name='delete_expense'),
    path('search-expense', csrf_exempt(views.SearchExpenseView.as_view()), name='search_expense'),
    path('summary-expense', views.SummaryExpenseView.as_view(), name='summary_expense'),
    path('expense-category-summary', views.expense_category_summary, name='expense-category-summary'),
    path('export_csv', views.export_csv, name='export_csv'),
    path('export_excel', views.export_excel, name='export_excel'),
    # path('export_pdf', views.export_pdf, name='export_pdf'),
]
