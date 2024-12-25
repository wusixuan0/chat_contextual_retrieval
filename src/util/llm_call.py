import os
import re
from anthropic import Anthropic
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

def get_completion(content, model_name):
    if re.search(r"gemini", model_name):            
        GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
        if not GEMINI_API_KEY: print("GEMINI_API_KEY not found")
        model_name = "gemini-1.5-flash" # "gemini-2.0-flash-exp"

        genai.configure(api_key=GEMINI_API_KEY)

        model = genai.GenerativeModel(model_name)
        response = model.generate_content(
            content,
            generation_config = genai.GenerationConfig(
                max_output_tokens=1000,
            )
        )
        print(response.text)
        return response.text

    elif re.search(r"grok", model_name):
        XAI_API_KEY = os.getenv('XAI_API_KEY')
        if not XAI_API_KEY: print("XAI_API_KEY not found")
        client = Anthropic(
            api_key=XAI_API_KEY,
            base_url="https://api.x.ai",
        )

        response = _get_sonnet(client, "grok-beta", content)
        print(response.content[0].text)
        return response.content[0].text

    elif model_name in ("claude-3-5-sonnet-20241022", "claude-3-haiku-20240307"):
        client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        response = _get_sonnet(client, model_name, content)
        return response.content[0].text

def _anthropic_sdk(client, model, content):
    
    response = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[
            {"role": "user", "content": content}
        ]
    )
    return response
