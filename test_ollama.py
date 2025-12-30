import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
print(OLLAMA_API_KEY)

client = OpenAI(
    base_url="https://ollama.com/v1",
    api_key=OLLAMA_API_KEY,
)

stream = client.chat.completions.create(
    model="gemma3:27b-cloud",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"},
    ],
    stream=True,
)

for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="", flush=True)