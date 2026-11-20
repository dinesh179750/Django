from django.shortcuts import render 
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.
def index(request):
    if request.method == "POST":
        name = request.POST.get('name')
        mail = request.POST.get('mail')
        desc = request.POST.get('desc')
        send_mail(
            f"hi {name} ",
            f" Your complaint \n{desc} \n been noted \n Our team will reach out you \n Regards \n Help team",
            settings.EMAIL_HOST_USER,
            {mail},
            fail_silently=False
        )
        return HttpResponse("mail sent")
    return render(request,"index.html")