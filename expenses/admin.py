from django.contrib import admin
from .models import Expense, Category

# Register your models here.
class ExpenseAdmin(admin.ModelAdmin):
    # https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display
    def get_category(self, obj):
        return obj.get_category_display()

    get_category.short_description = 'category'

    # https://stackoverflow.com/questions/16235201/list-display-how-to-display-value-from-choices
    list_display = ['amount', 'description', 'owner', 'get_category', 'date']
    # list_editable = 
    list_per_page = 5

admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Category)