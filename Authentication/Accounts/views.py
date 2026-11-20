from django.shortcuts import render, redirect
from .forms import RegistrationForm, RecaptchaForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout

# Create your views here.

def register(request):
    form = RegistrationForm()
    form1 = RecaptchaForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        form1 = RecaptchaForm(request.POST)
        if form.is_valid() and form1.is_valid():
            form.save()
            print("happy diwali")
            return redirect("signin")
        else:
            print("FORM ERRORS:",form.errors)
            print("CAPTCH ERRORS:",form1.errors)
    context = {
        'form': form,
        'form1': form1
    }
    return render(request, "register.html", context)


def signin(request):
    if request.method == "POST":
        un = request.POST.get('un')
        pswd = request.POST.get('pswd')
        a = None
        try:
            a = User.objects.get(username=un)
        except Exception as e:
            messages.error(request, "user does not exist")
        else:
            print("user found", a)

        if a:
            user = authenticate(request, username=un, password=pswd)
            print(user)
            if user:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Invalid password")

    return render(request, "signin.html")


def log_out(request):
    logout(request)
    return redirect("signin")