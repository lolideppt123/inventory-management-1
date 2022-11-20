from django.contrib import admin
from .models import Income, Source

# Register your models here.
class IncomeAdmin(admin.ModelAdmin):
    list_display = ['amount', 'description', 'owner', 'source', 'date']

admin.site.register(Income, IncomeAdmin)
admin.site.register(Source)