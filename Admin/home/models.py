from django.db import models

# Create your models here.
class teams(models.Model):
    name=models.CharField(max_length=32)
    fullform=models.CharField(max_length=50)
    owner=models.CharField(max_length=32)
    cap=models.CharField(max_length=32)
    coach=models.TextField()
    homeground_loc=models.TextField()
    cups=models.IntegerField()
    sponsors=models.TextField()
    reached_final=models.IntegerField()
    networth_of_team=models.IntegerField()

    def __str__(self):
        return self.name