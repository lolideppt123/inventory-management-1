from django.db import models

# Create your models here.
from random import choices
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.
class Income(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=15)
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.PROTECT)
    source = models.CharField(max_length=250)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.source


class Source(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
    