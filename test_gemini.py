import os

from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Read API Key
api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key)

# Test request
response = client.models.generate_content(
    model="models/gemini-flash-latest",
    contents="Reply with only one word: Hello"
)

print("=" * 50)
print("Gemini Response")
print("=" * 50)

print(response.text)