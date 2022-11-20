from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('', views.IndexPageView.as_view(), name='sales'),
    path('add-sale', views.AddSaleView.as_view(), name='add_sales'),
    path('customer-upload', views.customeruploadcsv, name='customer_upload'),
]