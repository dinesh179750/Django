from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class To_Do(models.Model):
    task = models.CharField(max_length=100)
    desc=models.TextField() 
    user = models.ForeignKey(User,on_delete=models.CASCADE)
