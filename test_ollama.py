import os
import base64
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
print(OLLAMA_API_KEY)

def encode_image(image_path):
    """Helper function to convert local image to base64."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# cloud url: https://ollama.com/v1
# local url: http://localhost:11434/v1
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key=OLLAMA_API_KEY,
)

image_path = "./image_sample.jpg"
base64_image = encode_image(image_path)

stream = client.chat.completions.create(
    model="gemma3:12b",
    messages=[
        {"role": "user", 
         "content": [
            {"type": "text", "text": "Describe the image."},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpg;base64,{base64_image}"
                },
            },
         ]},
    ],
    stream=True,
)

for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="", flush=True)