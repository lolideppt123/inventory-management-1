from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'incomes'

urlpatterns = [
    path('', views.IndexPageView.as_view(), name='incomes'),
    path('add_income', views.AddIncomeView.as_view(), name='add_income'),
    path('edit-income/<id>', views.EditIncomeView.as_view(), name='edit_income'),
    path('delete-income/<id>', views.DeleteIncomeView.as_view(), name='delete_income'),
    path('search-income', csrf_exempt(views.SearchIncomeView.as_view()), name='search_income'),
]
