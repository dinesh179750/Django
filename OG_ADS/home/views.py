from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'home.html')
def santoor(request):
    return render(request,'santoor.html')
def star(request):
    return render(request,'star.html')
def nirma(request):
    return render(request,'nirma.html')
def glucose(request):
    return render(request,'glucose.html')
def gems(request):
    return render(request,'gems.html')
def centerfruit(request):
    return render(request,'centerfruit.html')