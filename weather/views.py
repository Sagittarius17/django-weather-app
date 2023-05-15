import requests
from django.shortcuts import render
from .models import City

# Create your views here.

def index(request):
    cities = City.objects.all()

    weather_data = []

    for city in cities:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=d2e535af4bbcdabcac6c5b06b263c928'
        response = requests.get(url)
        data = response.json()

        city_weather = {
            'city': city.name,
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    context = {'weather_data': weather_data}
    return render(request, 'weather/index.html', context)
