# import json to load json data to python dictionary
import json
# urllib.request to make a request to api
import urllib.request
from django.shortcuts import render


def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        # api key might be expired use your own api_key
        # place api_key in place of appid ="your_api_key_here"

        # source contain JSON data from API

        source = urllib.request.urlopen(
            'http://api.openweathermap.org/data/2.5/weather?q ='
            + city + '&appid = d2e535af4bbcdabcac6c5b06b263c928').read()
        print(source)

        # converting JSON data to a dictionary
        list_of_data = json.loads(source)
        print(list_of_data)

        # data for variable list_of_data
        data = {
            "city": list_of_data['name'],
            "country_code": list_of_data['sys']['country'],
            "coordinate": str(list_of_data['coord']['lon']) + ' ' + str(list_of_data['coord']['lat']),
            "temp": str(list_of_data['main']['temp']) + 'K',
            "pressure": str(list_of_data['main']['pressure']),
            "humidity": str(list_of_data['main']['humidity']),
            "description": list_of_data['main'][0]['description'],
            "icon": list_of_data['weather'][0]['icon'],
        }
        print(data)
    else:
        data = {}
    return render(request, "main/index.html", data)
