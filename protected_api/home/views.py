import requests
from django.conf import settings
from django.shortcuts import render

def index(request):
    data = None
    if request.method == "POST":
        city = request.POST.get('city')
        if city:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={settings.API_KEY}&units=metric"
            response = requests.get(url)
            data = response.json()
            print(data)

    return render(request, "index.html", {"data": data})
