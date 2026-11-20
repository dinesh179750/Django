from django.db import models

# Create your models here.

class Travel(models.Model):
    name=models.CharField(max_length=35)
    source=models.CharField(max_length=100)
    destination=models.CharField(max_length=100)
    seats=models.PositiveIntegerField()
    start_date=models.DateField