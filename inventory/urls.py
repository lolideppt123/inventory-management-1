from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'inventory'

urlpatterns = [
    path('', views.IndexPageView.as_view(), name='inventory'),
    path('raw-materials/', views.RawMaterialsView.as_view(), name='raw_materials'),
    path('finished-goods/', views.FinishedGoodsView.as_view(), name='finished_goods'),
    path('add-inventory/', csrf_exempt(views.AddInventoryView.as_view()), name='add_inventory'),
    path('inventory-history/', csrf_exempt(views.InventoryHistoryView.as_view()), name='inventory_history'),
    path('edit-inventory-history/<id>', csrf_exempt(views.EditInventoryHistoryView.as_view()), name='edit_inventory_history'),
    
    # path('add_income', views.AddIncomeView.as_view(), name='add_income'),
    # path('edit-income/<id>', views.EditIncomeView.as_view(), name='edit_income'),
    # path('delete-income/<id>', views.DeleteIncomeView.as_view(), name='delete_income'),
    # path('search-income', csrf_exempt(views.SearchIncomeView.as_view()), name='search_income'),
]