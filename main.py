from openai import OpenAI
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

# Create an OpenAI client
client = OpenAI()

# Send a request to the LLM
response = client.responses.create(
    model="gpt-5.6-luna",
    input="Explain what an API is in one simple sentence."
)

# Print the LLM's answer
print(response.output_text)