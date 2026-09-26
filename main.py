import requests

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 32.7767,
    "longitude": -96.7970,
    "current": "temperature_2m"
}

response = requests.get(url, params=params)

data = response.json()

temperature = data["current"]["temperature_2m"]
unit = data["current_units"]["temperature_2m"]

print(f"Current temperature: {temperature}{unit}")