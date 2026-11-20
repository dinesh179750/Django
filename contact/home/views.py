from django.shortcuts import render
from .models import contacts
# Create your views here.
def home(request):
    phone = contacts.objects.all()

    context = {
        "phone": phone
    }

    return render(request, 'home.html', context)