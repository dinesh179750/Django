from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import To_do_Forms
from .models import To_Do
# Create your views here.

@login_required(login_url="signin")
def index(request):
    form=To_do_Forms()
    if request.method == "POST":
        task=request.POST.get("task")
        desc=request.POST.get("desc")
        To_Do.objects.create(task=task,desc=desc,user=request.user)
    context={
            'form':form
        }
    return render(request,"home.html",context)


@login_required(login_url="signin")
def display(request):
        data=To_Do.objects.filter(user=request.user)
        context={
            'data':data
        }
        return render(request,"display.html",context)