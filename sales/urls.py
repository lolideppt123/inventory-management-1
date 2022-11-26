from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'sales'

urlpatterns = [
    path('', views.IndexPageView.as_view(), name='sales'),
    path('add-sale', csrf_exempt(views.AddSaleView.as_view()), name='add_sales'),
    path('customer-upload', views.customeruploadcsv, name='customer_upload'),
]