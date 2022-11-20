from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.
class Expense(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=15)
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.PROTECT)
  
    CATEGORIES = [
        ('INSURANCE', 'Car Insurance'),
        ('RENTAL', 'House Rental'),
        ('Food', (
                ('GROCERY', 'Grocery'),
                ('ORDER', 'Food Order')
            )
        ),
        ('LOAN', 'Car Loan'),
    ]

    category = models.CharField(max_length=250, choices=CATEGORIES, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.category


class Category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'