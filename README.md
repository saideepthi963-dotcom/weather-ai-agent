# AI Weather Agent

A beginner-friendly AI agent built with Python that uses an LLM and a weather API to answer weather questions in natural language.

This project demonstrates how an AI agent can decide when it needs an external tool, call that tool, retrieve real-world data, and use the result to generate a natural-language response.

## Features

- Ask for the current weather in a city
- Retrieves live weather data using the Open-Meteo API
- Uses an OpenAI language model to generate natural responses
- Uses function/tool calling so the LLM can decide when weather data is needed
- Returns temperature, humidity, weather conditions, and wind speed
- Maintains conversation context for follow-up questions
- Handles invalid cities and API/network errors
- Supports normal non-weather questions without calling the weather tool

## How It Works

The basic flow is:

```text
User
  ↓
Python Application
  ↓
LLM
  ↓
Does the LLM need weather data?
  ↓
Weather Tool
  ↓
Open-Meteo API
  ↓
Weather Data
  ↓
LLM
  ↓
Natural-Language Response
  ↓
User
```

The LLM does not directly fetch the weather.

Instead, it decides when the `get_weather` tool should be used. The Python application executes the tool, retrieves the weather data from Open-Meteo, and sends the result back to the LLM.

## Technologies Used

- Python
- OpenAI API
- Open-Meteo API
- Requests
- python-dotenv
- JSON
- Git and GitHub

## Project Structure

```text
weather-ai-agent/
├── .env
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

The `.env` file is stored locally and is excluded from GitHub using `.gitignore`.

## Installation

Clone the repository and move into the project directory.

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project directory.

Add your OpenAI API key:

```text
OPENAI_API_KEY=your_api_key_here
```

Do not commit your `.env` file or API key to GitHub.

## Run the Agent

Run:

```bash
python main.py
```

Then ask a question:

```text
You: What is the weather in Dallas?
```

Example response:

```text
LLM decided to use a tool.
Tool result: Current weather in Dallas: temperature 26.2°C, humidity 68%, condition Clear sky, wind speed 12.0 km/h.
AI: Dallas is currently 26.2°C with clear skies. Humidity is 68%, with winds around 12 km/h.
```

The agent can also answer questions that do not require the weather tool:

```text
You: Explain SQL in one sentence.
LLM decided no tool was needed.
AI: SQL (Structured Query Language) is a language used to create, read, update, and manage data in relational databases.
```

Type `exit` to stop the program.

## Concepts Learned

This project demonstrates:

- APIs and API requests
- JSON responses
- Large Language Models (LLMs)
- Function/tool calling
- AI agent architecture
- Conversation context
- Error handling
- Environment variables
- Git and GitHub workflow
- Organizing Python code into functions

## Security

API keys should never be stored directly in source code.

This project loads the OpenAI API key from a local `.env` file. The `.env` file is included in `.gitignore` so credentials are not uploaded to GitHub.

## Future Improvements

Possible future improvements include:

- Weather forecasts
- Multiple tool calls
- Additional tools and APIs
- More robust response handling
- A web-based user interface
- Persistent conversation memory