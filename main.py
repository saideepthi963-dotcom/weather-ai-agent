import requests
import json
from openai import OpenAI
from dotenv import load_dotenv


class geocoding_response:
    """Small wrapper around the Open-Meteo geocoding API."""

    def __init__(self, city):
        self.city = city
        self.latitude = None
        self.longitude = None
        self.raw_data = {}

    def fetch(self):
        geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
        geocoding_params = {"name": self.city, "count": 1}

        try:
            response = requests.get(
                geocoding_url,
                params=geocoding_params,
                timeout=10,
            )
            response.raise_for_status()
        except requests.RequestException:
            raise ValueError(f"Could not connect to the location service for {self.city}.")

        self.raw_data = response.json()
        results = self.raw_data.get("results")
        if not results:
            raise ValueError(f"Could not find a city named {self.city}.")

        first_result = results[0]
        self.latitude = first_result["latitude"]
        self.longitude = first_result["longitude"]
        return {"latitude": self.latitude, "longitude": self.longitude}

    def get_coordinates(self):
        if self.latitude is None or self.longitude is None:
            self.fetch()
        return self.latitude, self.longitude


def get_weather_description(code):
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        95: "Thunderstorm"
    }

    return weather_codes.get(code, "Unknown weather condition")

def get_weather(city):
    # Step 1: Convert city name into latitude and longitude
    try:
        geocoding = geocoding_response(city)
        latitude, longitude = geocoding.get_coordinates()
    except ValueError as exc:
        return str(exc)

    # Step 2: Get weather using those coordinates
    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "weather_code",
            "wind_speed_10m"
        ]
    }

    try:
        weather_response = requests.get(
            weather_url,
            params=weather_params,
            timeout=10,
        )
        weather_response.raise_for_status()
    except requests.RequestException:
        return f"Could not retrieve weather data for {city}."

    weather_data = weather_response.json()

    if "current" not in weather_data:
        return f"Could not retrieve weather data for {city}."

    temperature = weather_data["current"]["temperature_2m"]
    humidity = weather_data["current"]["relative_humidity_2m"]
    weather_code = weather_data["current"]["weather_code"]
    weather_description = get_weather_description(weather_code)
    wind_speed = weather_data["current"]["wind_speed_10m"]

    temperature_unit = weather_data["current_units"]["temperature_2m"]
    humidity_unit = weather_data["current_units"]["relative_humidity_2m"]
    wind_unit = weather_data["current_units"]["wind_speed_10m"]

    return (
        f"Current weather in {city}: "
        f"temperature {temperature}{temperature_unit}, "
        f"humidity {humidity}{humidity_unit}, "
        f"condition {weather_description}, "
        f"wind speed {wind_speed} {wind_unit}."
) 

load_dotenv()

client = OpenAI()

weather_tool = {
    "type": "function",
    "name": "get_weather",
    "description": "Get the current temperature for a city.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "The city to get the weather for."
            }
        },
        "required": ["city"]
    }
}
previous_response_id = None
while True:

    user_question = input("\nYou: ")

    # Stop the program if the user types exit
    if user_question.lower() == "exit":
        print("AI: Goodbye!")
        break

    response = client.responses.create(
    model="gpt-5.6-luna",
    input=user_question,
    tools=[weather_tool],
    previous_response_id=previous_response_id
)

    output = response.output[0]

    # Check whether the LLM wants to use a tool
    if output.type == "function_call":

        print("LLM decided to use a tool.")

        arguments = json.loads(output.arguments)

        city = arguments["city"]

        weather_result = get_weather(city)

        print("Tool result:", weather_result)

        final_response = client.responses.create(
            model="gpt-5.6-luna",
            previous_response_id=response.id,
            input=[
                {
                    "type": "function_call_output",
                    "call_id": output.call_id,
                    "output": weather_result
                }
            ],
            tools=[weather_tool]
        )

        print("AI:", final_response.output_text)
        previous_response_id = final_response.id

    else:
        print("LLM decided no tool was needed.")

        if response.output_text:
            print("AI:", response.output_text)
            previous_response_id = response.id
        else:
            print("AI: I couldn't generate a response for that request.")

  