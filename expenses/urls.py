from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    path('', views.index, name='expenses'),
    path('add_expense', views.add_expense, name='add_expense'),
]