from django.db import models

# Create your models here.
class Crackers(models.Model):
    cracker_name=models.CharField(max_length=100)
    price=models.PositiveIntegerField()
    Quantity=models.PositiveIntegerField()
    Age_range=models.TextField()
    choices=[
        ('a',"Galoo"),
        ("b","Bhumida")
    ]
    type_of_cracker=models.CharField(max_length=1,choices=choices)
    image=models.ImageField(upload_to="Assets")


class Sweets(models.Model):
    Sweet_name=models.CharField(max_length=35)
    price=models.PositiveIntegerField()
    choices=[
        ('kg',"Kilogram"),
        ('hkg',"half-kilogram")
    ]
    Quantity_in=models.CharField(max_length=3,choices=choices)
    image=models.ImageField(upload_to="Assets")


class Gifts(models.Model):
    Gift_name=models.CharField(max_length=35)
    image=models.ImageField(upload_to="Assets")
    price=models.PositiveIntegerField()
    quantity=models.PositiveIntegerField()