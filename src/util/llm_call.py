import os
import google.generativeai as genai
from dotenv import load_dotenv
import time
from ratelimit import limits, sleep_and_retry

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY: print("GEMINI_API_KEY not found")

genai.configure(api_key=GEMINI_API_KEY)
generation_config = {
    "max_output_tokens": 250,
}
model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

@sleep_and_retry
@limits(calls=10, period=60)
def get_llm(content):
    start_time = time.time()
    try:
        response = model.generate_content(content)
        end_time = time.time()
        print(f"Time taken: {end_time - start_time} seconds")
        print(response.text)
        return response.text
    except Exception as e:
        print(f"Error during Gemini API call: {e}")
