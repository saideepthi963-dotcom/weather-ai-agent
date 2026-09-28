import requests
import json
import requests
from openai import OpenAI
from dotenv import load_dotenv

def get_weather(city):
    # Step 1: Convert city name into latitude and longitude
    geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"

    geocoding_params = {
        "name": city,
        "count": 1
    }

    geocoding_response = requests.get(
        geocoding_url,
        params=geocoding_params
    )

    geocoding_data = geocoding_response.json()

    latitude = geocoding_data["results"][0]["latitude"]
    longitude = geocoding_data["results"][0]["longitude"]

    # Step 2: Get weather using those coordinates
    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m"
    }

    weather_response = requests.get(
        weather_url,
        params=weather_params
    )

    weather_data = weather_response.json()

    temperature = weather_data["current"]["temperature_2m"]
    unit = weather_data["current_units"]["temperature_2m"]

    return f"The current temperature in {city} is {temperature}{unit}"

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
        print("AI:", response.output_text)
        previous_response_id = response.id