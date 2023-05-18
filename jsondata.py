import requests
import json

url = "http://api.openweathermap.org/data/2.5/weather?id=524901&appid=d2e535af4bbcdabcac6c5b06b263c928"  # Replace with the actual API endpoint

# Make a GET request to the API
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    data = response.json()  # Extract the JSON data from the response
    # Now you can work with the JSON data as a Python dictionary
    print(data)
else:
    print("Request failed with status code:", response.status_code)
    
filename = "data.json"  # Specify the desired filename

# Open the file in write mode
with open(filename, "w") as file:
    json.dump(data, file)
