from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/authentication/login')
def hompageview(request):
    
    return render(request, 'dashboard/homepage.html')