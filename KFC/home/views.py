from django.shortcuts import render,HttpResponse

# Create your views here.
def index(request):
    return HttpResponse('''
<div style:"display:flex;"><img src='https://online.kfc.co.in/static/media/kfcLogo.492728c6.svg'><h3>Home</h3><h3>Meals</h3></div>''')