import json
import urllib.request
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
    if request.method == 'POST':
        city = request.POST['city']

        # Construct the API request URL with the city parameter
        url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=d2e535af4bbcdabcac6c5b06b263c928'
        
        try:
            # Make the API request
            response = urllib.request.urlopen(url)
            
            # Read the response data
            data = response.read().decode('utf-8')
            
            # Convert JSON data to a dictionary
            list_of_data = json.loads(data)

            # Extract the required weather data from the dictionary
            data = {
                "city": list_of_data['name'],
                "country_code": list_of_data['sys']['country'],
                "coordinate": str(list_of_data['coord']['lon']) + ' ' + str(list_of_data['coord']['lat']),
                "temp": str(list_of_data['main']['temp']) + 'K',
                "pressure": str(list_of_data['main']['pressure']),
                "humidity": str(list_of_data['main']['humidity']),
                "description": list_of_data['weather'][0]['description'],
                "icon": list_of_data['weather'][0]['icon'],
            }
            
            # Render the response with the weather data
            return render(request, "weatherapp/index.html", data)
        
        except urllib.error.HTTPError as e:
            # Handle HTTP errors
            return render(request, "weatherapp/error.html", {'error': str(e)})
        
        except Exception as e:
            # Handle other exceptions
            return render(request, "weatherapp/error.html", {'error': str(e)})
    
    else:
        # Render the form initially without weather data
        return render(request, "weatherapp/index.html")
