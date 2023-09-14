from django.shortcuts import render
import requests
import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
# def index(request):
#     api_key = 'd2e535af4bbcdabcac6c5b06b263c928'
#     current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?city={city}&appid={api_key}'
#     forecast_url = 'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly,alerts&appid={api_key}'

#     if request.method == 'POST':
#         city = request.POST.get('city')
#         # city2 = request.POST.get('city2', None)

#         weather_data, daily_forecasts = fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url)

#         # if city2:
#         #     weather_data2, daily_forecasts2 = fetch_weather_and_forecast(city2, api_key, current_weather_url, forecast_url)
#         # else:
#         #     weather_data2, daily_forecasts2 = None, None

#         context = {
#             'weather_data': weather_data,
#             'daily_forecasts': daily_forecasts,
#             # 'weather_data2': weather_data2,
#             # 'daily_forecasts2': daily_forecasts2,
#         }

#         return render(request, 'weatherapp/index.html', context)
#     else:
#         return render(request, 'weatherapp/index.html')


# def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
#     formatted_url = current_weather_url.format(city=city, api_key=api_key)
#     response = requests.get(formatted_url)
#     if response.status_code != 200:
#         print(f"Error: Received status code {response.status_code}")
#         print(response.json())  # This will print the error details (if any) provided by the API.
#         return None, None
    
#     lat, lon = response['coord']['lat'], response['coord']['lon']
#     forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()
#     print(forecast_response)

#     weather_data = {
#         'city': city,
#         'temperature': round(response['main']['temp'] - 273.15, 2),
#         'description': response['weather'][0]['description'],
#         'icon': response['weather'][0]['icon'],
#     }

#     daily_forecasts = []
#     for daily_data in forecast_response['daily'][:5]:
#         daily_forecasts.append({
#             'day': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
#             'min_temp': round(daily_data['temp']['min'] - 273.15, 2),
#             'max_temp': round(daily_data['temp']['max'] - 273.15, 2),
#             'description': daily_data['weather'][0]['description'],
#             'icon': daily_data['weather'][0]['icon'],
#         })

#     return weather_data, daily_forecasts

def index(request):
    # Use your OpenWeatherMap API key here
    API_KEY = "d2e535af4bbcdabcac6c5b06b263c928"
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    city = request.POST.get('city')

    params = {
        'q': city,
        'appid': API_KEY,
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        weather_data = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"],
        }
        # return JsonResponse(weather_data)
        return render(request, 'weatherapp/index.html', weather_data)
    else:
        return JsonResponse({"error": "Could not fetch weather data."})