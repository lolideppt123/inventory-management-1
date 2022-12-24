from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'sales'

urlpatterns = [
    path('', views.IndexPageView.as_view(), name='sales'),
    path('add-sale', csrf_exempt(views.AddSaleView.as_view()), name='add_sales'),
    path('edit-sale/<id>', views.EditSaleView.as_view(), name='edit_sales'),
    path('search-sales', csrf_exempt(views.SearchSalesView.as_view()), name='search_sales'),
    path('sales-statistics', views.SalesStatisticsView.as_view(), name='sales_statistics'),
    path('product-sales-summary', csrf_exempt(views.product_sales_summary), name='product_sales_summary'),
    path('customer-sales-summary', csrf_exempt(views.customer_sales_summary), name='customer_sales_summary'),
    
    path('customer-upload', views.customeruploadcsv, name='customer_upload'),
    path('product-upload', views.productuploadcsv, name='product_upload'),
    path('sales-upload', views.salesuploadcsv, name='sales_upload'),
]