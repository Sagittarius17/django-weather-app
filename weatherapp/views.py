from django.shortcuts import render
import requests
import datetime
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
    api_key = '09f07301cd82ad99e41e029a6e9d6afb'
    current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    forecast_url = 'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}'
    # forecast_url = "https://api.openweathermap.org/data/2.5/onecall?lon={lon}&lat={lat}&exclude=current,minutely,hourly,alerts&appid={api_key}"

    if request.method == 'POST':
        city = request.POST.get('city')
        city2 = request.POST.get('city2', None)

        # weather_data = fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url)
        # daily_forecasts = fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url)
        weather_data, daily_forecasts = fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url)


        if city2:
            # weather_data2 = fetch_weather_and_forecast(city2, api_key, current_weather_url, forecast_url)
            # daily_forecasts2 = fetch_weather_and_forecast(city2, api_key, current_weather_url, forecast_url)
            weather_data2, daily_forecasts2 = fetch_weather_and_forecast(city2, api_key, current_weather_url, forecast_url)
        else:
            weather_data2, daily_forecasts2 = None, None

        context = {
            'weather_data': weather_data,
            'daily_forecasts': daily_forecasts,
            'weather_data2': weather_data2,
            'daily_forecasts2': daily_forecasts2,
        }

        return render(request, 'weatherapp/index.html', context)
    else:
        return render(request, 'weatherapp/index.html')


def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    formatted_url = current_weather_url.format(city=city, api_key=api_key)
    response = requests.get(formatted_url)
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        return None, None
    
    response_data = response.json()
    print("Response data:", response_data)
    
    # Check if the 'coord' key exists and if it has both 'lat' and 'lon' keys
    if 'coord' in response_data and 'lon' in response_data['coord'] and 'lat' in response_data['coord']:
        lon, lat = response_data['coord']['lon'], response_data['coord']['lat']
    else:
        # Log the error for debugging purposes
        # print("Error: Invalid response data:", response_data)
        return None, None
    
    forecast_response = requests.get(forecast_url.format(lon=lon, lat=lat, api_key=api_key))
    # print("Forecast Response:", forecast_response.text)

    if forecast_response.status_code != 200:
        print(f"Error fetching forecast: {forecast_response.status_code} - {forecast_response.json()}")
        return None, None
    
    forecast_data = forecast_response.json()
    # print("Forecast Data:", forecast_data)
    today = datetime.date.today()
    weather_data = {
        'city': city,
        'date': today,
        'temperature': round(response_data['main']['temp'] - 273.15, 2),
        'min_temp': round(response_data['main']['temp_min'] - 273.15, 2),
        'max_temp': round(response_data['main']['temp_max'] - 273.15, 2),
        'description': response_data['weather'][0]['description'],
        'icon': response_data['weather'][0]['icon'],
    }

    daily_forecasts = []
    for daily_data in forecast_data['list'][:40]:
        daily_forecasts.append({
            'day': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
            'date': daily_data['dt_txt'],
            'min_temp': round(daily_data['main']['temp_min'] - 273.15, 2),
            'max_temp': round(daily_data['main']['temp_max'] - 273.15, 2),
            'description': daily_data['weather'][0]['description'],
            'icon': daily_data['weather'][0]['icon'],
        })

    return weather_data, daily_forecasts
