from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Agent, Investigate

admin.site.register(Agent)
admin.site.register(Investigate)
