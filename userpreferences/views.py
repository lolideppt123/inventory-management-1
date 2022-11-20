from django.shortcuts import render
from django.views import View
from django.conf import settings
from .models import UserPreference
from django.contrib import messages
import os, json

# Create your views here.
class IndexPage(View):
    file_path = os.path.join(settings.BASE_DIR, 'currency.json')

    with open(file_path, 'r') as currency_json:
        currency_list = json.load(currency_json)

    def get(self, request):
        # # debugger it will pause and run debugger
        # import pdb
        # pdb.set_trace()
        exist = UserPreference.objects.filter(user=request.user).exists()
        if exist:
            user_preference = UserPreference.objects.get(user=request.user)
            return render(request, 'preferences/index.html', {'currencies':self.currency_list, 'user_preference': user_preference})
        return render(request, 'preferences/index.html', {'currencies':self.currency_list})

    def post(self, request):
        exist = UserPreference.objects.filter(user=request.user).exists()
        currency = request.POST['currency']
        user_preference = None

        if exist:
            user_preference = UserPreference.objects.get(user=request.user)
            user_preference.currency = currency
            user_preference.save()
        else:
            UserPreference.objects.create(user=request.user, currency=currency)
        messages.success(request, 'Changes saved.')
        # import pdb
        # pdb.set_trace()

        return render(request, 'preferences/index.html', {'currencies':self.currency_list, 'user_preference': user_preference})