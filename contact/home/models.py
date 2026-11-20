from django.db import models

# Create your models here.
class contacts(models.Model):
    name=models.CharField(max_length=25)
    company=models.CharField(max_length=25,null=True, blank=True)
    phone_number = models.CharField(max_length=10)
    email=models.CharField(max_length=30,null=True, blank=True)
    address=models.TextField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name
