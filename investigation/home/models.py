from django.db import models


class Agent(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Investigate(models.Model):

    case_id = models.IntegerField(primary_key=True)

    case_description = models.TextField(null=True)

    case_type = models.CharField(max_length=30)

    loc = models.TextField()

    complaint_name = models.CharField(max_length=40)

    assigned_agent = models.ForeignKey(
        Agent,
        on_delete=models.CASCADE
    )

    case_status = models.CharField(max_length=10)