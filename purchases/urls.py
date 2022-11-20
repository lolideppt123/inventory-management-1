from django.urls import path
from . import views

app_name = 'purchases'

urlpatterns = [
    path('', views.IndexPageView.as_view(), name='purchases'),
    path('add-purchase', views.AddPurchaseView.as_view(), name='add_purchase'),
]
